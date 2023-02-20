TOOLS_GIT = git@github.com:viktorsboroviks/tools.git
TOOLS_BRANCH = 6ceeefe9f2bdba83a9a8aaa003431146ba577fe5
TOOLS_PATH = tools
TABLES = \
		article/abs_change.csv \
		article/rel_change.csv
DIAGRAMS = \
		article/diag_p1_p2_dec.pdf \
		article/diag_p1_p2_inc.pdf \
		article/diag_p1_p2_p3_inc.pdf \
		article/diag_p1_p2_p3_dec.pdf \
		article/abs_change_rate1.pdf \
		article/abs_change_rate2.pdf \
		article/rel_change_rate1.pdf \
		article/rel_change_rate2.pdf \
		article/rel_osc_inc.pdf \
		article/rel_osc_dec.pdf \
		article/rel_osc_inc_n150.pdf
EXAMPLES = \
		python/abs_change.csv \
		python/rel_change.csv \
		python/abs_change_rate1.svg \
		python/abs_change_rate2.svg \
		python/rel_change_rate1.svg \
		python/rel_change_rate2.svg \
		python/rel_osc_inc.svg \
		python/rel_osc_dec.svg \
		python/rel_osc_inc_n150.svg

.PHONY: all setup article clean distclean
all: article

$(TOOLS_PATH):
	git clone $(TOOLS_GIT) $(TOOLS_PATH)
	cd $(TOOLS_PATH); git checkout $(TOOLS_BRANCH)

setup: $(TOOLS_PATH)
	make setup-fin setup-latex --directory $(TOOLS_PATH)
	cd python; ../$(TOOLS_PATH)/docker/finpy.sh examples.py

article/%.pdf: inkscape/%.svg
	./$(TOOLS_PATH)/docker/svg2pdf.sh \
		"$<" \
		"$@"

article/%.pdf: python/%.svg
	./$(TOOLS_PATH)/docker/svg2pdf.sh \
		"$<" \
		"$@"

article/%.csv: python/%.csv
	mv "$<" "$@"

article: setup $(EXAMPLES) $(TABLES) $(DIAGRAMS)
# run pdflatex twice to generate proper references to figures and equations
# (yes, this is how Latex works)
	cd article && \
		../$(TOOLS_PATH)/docker/pdflatex.sh article.tex && \
		../$(TOOLS_PATH)/docker/pdflatex.sh article.tex
	mv article/article.pdf article.pdf

# remove temporary files
clean:
	if [ -d "$(TOOLS_PATH)" ]; then \
		$(TOOLS_PATH)/native/clean_latex.sh -v . ;\
	fi
	rm -rfv __pycache__ python/__pycache__

# remove all files produced by `make`
distclean: clean
	rm -rfv $(TOOLS_PATH)
	rm -fv $(EXAMPLES)
	rm -fv $(TABLES)
	rm -fv $(DIAGRAMS)
	rm -fv article.pdf
