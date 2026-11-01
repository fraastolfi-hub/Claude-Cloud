import json, subprocess, os, sys
V='/tmp/claude-0/-home-user-Claude-Cloud/1e980736-cb50-5140-90c7-927c92c44c9a/scratchpad/voce'
P='/tmp/claude-0/-home-user-Claude-Cloud/1e980736-cb50-5140-90c7-927c92c44c9a/scratchpad/video-romagna'
TEMPO=1.07
CFG={  # reel: (old slot starts, first-word index of each line, old content end = closing start, old total)
 'reel2':([0,2,6,11,14,17],[0,2,16,25,31,42],20),
 'reel3':([0,2,6,10,14,18,20],[0,10,21,28,32,45,56],22),
 'reel4':([0,2,6,10,13,17],[0,3,15,26,27,37],20),
 'reel7':([0,2,4,8,11,15],[0,5,8,18,29,38],18),
}
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
out={}
os.makedirs(f'{P}/public/voce',exist_ok=True)
for r,(O,idx,oldtot) in CFG.items():
    w=json.load(open(f'{V}/{r}.json'))['words']; total=dur(f'{V}/{r}.m4a')
    lines=[]
    for i,s in enumerate(idx):
        e=idx[i+1]-1 if i+1<len(idx) else len(w)-1
        a=w[s]['start']; b=w[e]['end']
        pa=w[s-1]['end'] if s>0 else 0
        nb=w[e+1]['start'] if e+1<len(w) else total
        a=max(a-0.15,(pa+a)/2); b=min(b+0.35,(b+nb)/2)
        f=f'{V}/{r}_l{i}.wav'
        subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{a:.3f}','-to',f'{b:.3f}','-i',f'{V}/{r}.m4a','-af',
          f'highpass=f=80,afftdn=nf=-25,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={TEMPO},afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse','-ar','48000','-ac','1',f],check=True)
        lines.append((f,dur(f)))
    N=[]; t=0.0
    for i,(f,L) in enumerate(lines):
        n=0.35 if i==0 else max(O[i], N[-1]+lines[i-1][1]+0.25)
        N.append(n)
    # keyframes new->old; first key 0->0
    keys=[[0,0]]+[[round(N[i],3),O[i]] for i in range(1,len(O))]
    newdur=max(N[-1]+(oldtot-O[-1]), N[-1]+lines[-1][1]+0.6)
    # mix
    args=['ffmpeg','-y','-v','error']; fl=[]
    for i,(f,L) in enumerate(lines):
        args+=['-i',f]; fl.append(f'[{i}]adelay={int(N[i]*1000)}:all=1[a{i}]')
    fl.append(''.join(f'[a{i}]' for i in range(len(lines)))+f'amix=inputs={len(lines)}:normalize=0,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7,apad,atrim=0:{newdur:.3f}[o]')
    args+=['-filter_complex',';'.join(fl),'-map','[o]','-ar','48000','-ac','2',f'{P}/public/voce/{r}.wav']
    subprocess.run(args,check=True)
    out[r]={'keys':keys,'dur':round(newdur,3),'oldDur':oldtot,'lines':[[round(N[i],2),round(L,2)] for i,(f,L) in enumerate(lines)]}
    print(r,out[r])
json.dump(out,open(f'{P}/src/reel/voce.json','w'),indent=1)
