paper.pdf: paper.tex plot-data.png
	tectonic paper.tex

plot-%.png: %.dat plot.py
	./plot.py -i $*.dat -o $@

.PHONY: clean
clean:
	rm -f plot-*.png paper.pdf
