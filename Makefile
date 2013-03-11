150mm_hawaii_mask.svg: Makefile

150mm_hawaii_mask.pgm: hawaii_mask.pgm
	pnmscale 0.0354 < $< > $@

%.svg: %.pgm
	potrace --invert --svg < $< | sed 's/fill="[^"]*/fill="none/;s/stroke="[^"]*/stroke="#000/' > $@
