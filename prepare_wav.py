"""Convert a short integer-PCM WAV to the camera's canonical 8k mono format.

No SD/camera writes. Also creates four original, procedurally synthesized
example clicks. No reference repository audio is redistributed.
"""
import argparse
import math
import random
import struct
import wave
from pathlib import Path


def encode(samples):
    data=struct.pack('<'+'h'*len(samples),*samples)
    return struct.pack('<4sI4s4sIHHIIHH4sI',b'RIFF',len(data)+36,b'WAVE',b'fmt ',16,1,1,8000,16000,2,16,b'data',len(data))+data


def prepare(source):
    with wave.open(str(source),'rb') as w:
        channels,width,rate,frames=w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes()
        if w.getcomptype()!='NONE' or width not in (1,2,3,4) or not (1<=channels<=8):
            raise ValueError('Input must be integer PCM WAV, 8/16/24/32-bit, 1..8 channels')
        if frames==0 or rate<=0 or frames/rate>1.08:
            raise ValueError('Use a nonempty sound of at most 1.08 seconds')
        raw=w.readframes(frames)
        if len(raw)!=frames*channels*width:raise ValueError('Truncated WAV')
    mono=[]
    for frame in range(frames):
        values=[]
        for channel in range(channels):
            pos=(frame*channels+channel)*width
            value=(raw[pos]-128)*256 if width==1 else int.from_bytes(raw[pos:pos+width],'little',signed=True)*2.0**(16-width*8)
            values.append(value)
        mono.append(sum(values)/channels)
    count=min(8640,max(1,round(frames*8000/rate)))
    result=[]
    for i in range(count):
        pos=i*rate/8000;lo=min(int(pos),frames-1);hi=min(lo+1,frames-1)
        value=mono[lo]+(mono[hi]-mono[lo])*(pos-lo)
        result.append(max(-32768,min(32767,round(value))))
    return encode(result)


def example(slot):
    rng=random.Random(530+slot)
    duration=(.12,.19,.14,.16)[slot-1]
    out=[]
    for i in range(round(duration*8000)):
        t=i/8000
        noise=rng.uniform(-1,1)
        if slot==4:
            value=math.sin(2*math.pi*1100*t)*math.exp(-t/0.025)
        else:
            value=(.55*noise+.3*math.sin(2*math.pi*680*t)+.15*math.sin(2*math.pi*1730*t))*math.exp(-t/(.009 if slot==1 else .014))
            if slot==2 and t>=.065:
                value+=.7*(noise+math.sin(2*math.pi*900*t))*.5*math.exp(-(t-.065)/.014)
            if slot==3:value*=.5
        value*=min(1,i/4)*min(1,(duration-t)*400)
        out.append(round(max(-1,min(1,value))*10000))
    return encode(out)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args()
    payload=prepare(a.source)
    with a.output.open('xb') as f:f.write(payload)
    print('Created',a.output,'8 kHz / mono / signed 16-bit /',len(payload),'bytes')
