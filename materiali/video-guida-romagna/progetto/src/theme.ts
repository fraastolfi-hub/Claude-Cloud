import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

loadFont({family: 'Outfit', url: staticFile('fonts/outfit.woff2'), weight: '100 900'});
loadFont({family: 'Figtree', url: staticFile('fonts/figtree.woff2'), weight: '300 900'});

export const C = {
  crema: '#faf7f4', ink: '#262521', ink2: '#57534c', giallo: '#ffd22e', lilla: '#8f8cff',
  lillaSoft: '#d8d6ff', teal: '#22a094', tealSoft: '#bfe8e3', rosa: '#ff93c7', rosaSoft: '#ffd3ea', gialloSoft: '#fff1b8',
};
export const display = 'Outfit';
export const text = 'Figtree';
loadFont({family: 'Caveat', url: staticFile('fonts/caveat.woff2'), weight: '700'});
export const hand = 'Caveat';
export const GIALLO_SUB = '#FFE600';
