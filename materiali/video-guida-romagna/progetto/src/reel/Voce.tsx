import React from 'react';
import {AbsoluteFill, Audio, Freeze, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import voce from './voce.json';
import {Reel2} from './Reel2';
import {Reel3} from './Reel3';
import {Reel4} from './Reel4';
import {Reel7} from './Reel7';

type Cfg = {keys: number[][]; dur: number; oldDur: number};
export const VOCE = voce as Record<string, Cfg>;

// la voce detta i tempi: ogni scena parte quando parte la sua battuta,
// l'animazione rallenta dove la voce è più lunga dello spazio previsto
const Warp: React.FC<{cfg: Cfg; children: React.ReactNode}> = ({cfg, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const k = [...cfg.keys, [cfg.keys[cfg.keys.length - 1][0] + 100, cfg.keys[cfg.keys.length - 1][1] + 100]];
  const old = interpolate(t, k.map((x) => x[0]), k.map((x) => x[1]));
  const f = Math.min(Math.round(old * fps), cfg.oldDur * fps - 1);
  return <Freeze frame={f}>{children}</Freeze>;
};

const make = (id: string, C: React.FC) => () => (
  <AbsoluteFill>
    <Warp cfg={VOCE[id]}><C /></Warp>
    <Audio src={staticFile(`voce/${id}.wav`)} />
  </AbsoluteFill>
);
export const Reel2Voce = make('reel2', Reel2);
export const Reel3Voce = make('reel3', Reel3);
export const Reel4Voce = make('reel4', Reel4);
export const Reel7Voce = make('reel7', Reel7);
