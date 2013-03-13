output/150mm_hawaii_0.svg: Makefile

# Results in an output file where 1mm = 1km (aka 1:1000000)
150mm_hawaii_0.pgm: hawaii_mask.pgm
	pnmscale 0.0354 < $< > $@

150mm_hawaii.pgm: hawaii.pgm
	pnmscale 0.0354 < $< > $@

etch: composed/hawaii_0.svg composed/hawaii_1.svg composed/hawaii_2.svg composed/hawaii_3.svg composed/hawaii_4.svg composed/hawaii_5.svg composed/hawaii_6.svg

layers: output/150mm_hawaii_0.svg output/150mm_hawaii_1.svg output/150mm_hawaii_2.svg output/150mm_hawaii_3.svg output/150mm_hawaii_4.svg output/150mm_hawaii_5.svg output/150mm_hawaii_6.svg

composed/hawaii_0.svg: output/150mm_hawaii_0.svg code/6composites
composed/hawaii_1.svg: output/150mm_hawaii_1.svg code/6composites
composed/hawaii_2.svg: output/150mm_hawaii_2.svg code/6composites
composed/hawaii_3.svg: output/150mm_hawaii_3.svg code/6composites
composed/hawaii_4.svg: output/150mm_hawaii_4.svg code/6composites
composed/hawaii_5.svg: output/150mm_hawaii_5.svg code/6composites
composed/hawaii_6.svg: output/150mm_hawaii_6.svg code/6composites

composed/hawaii_0.svg composed/hawaii_1.svg composed/hawaii_2.svg composed/hawaii_3.svg composed/hawaii_4.svg composed/hawaii_5.svg composed/hawaii_6.svg:
	code/6composites

output/150mm_hawaii_1.svg: 150mm_hawaii.pgm code/6layers
output/150mm_hawaii_2.svg: 150mm_hawaii.pgm code/6layers
output/150mm_hawaii_3.svg: 150mm_hawaii.pgm code/6layers
output/150mm_hawaii_4.svg: 150mm_hawaii.pgm code/6layers
output/150mm_hawaii_5.svg: 150mm_hawaii.pgm code/6layers
output/150mm_hawaii_6.svg: 150mm_hawaii.pgm code/6layers

output/150mm_hawaii_1.svg output/150mm_hawaii_2.svg output/150mm_hawaii_3.svg output/150mm_hawaii_4.svg output/150mm_hawaii_5.svg output/150mm_hawaii_6.svg:
	code/6layers $<

hawaii_mask.pgm:
	code/arctopnm.py

output/%.svg: %.pgm
	mkdir -p output
	potrace --invert --svg < $< | sed 's/fill="[^"]*/fill="none/;s/stroke="[^"]*/stroke="#000/' > $@
