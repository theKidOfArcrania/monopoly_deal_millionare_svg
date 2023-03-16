DPI ?= 300
SVGS = $(shell ls cards/*.svg)
PROPS_NORM = lb_1 lb_2 lb_3 m_1 m_2 m_3 o_1 o_2 o_3 r_1 r_2 r_3 \
				y_1 y_2 y_3 g_1 g_2 g_3
PROPS_2SET = br_1 br_2 b_1 b_2
PROPS_WILD = mo_1 ry_1
PROPS_2WILD = bb_1 gb_1
PROPS_GOLD = go_1 go_2 go_3
PROPS = $(PROPS_NORM:%=props/prop_n_%.svg) $(PROPS_GOLD:%=props/prop_g_%.svg) \
	$(PROPS_2SET:%=props/prop_2_%.svg) $(PROPS_WILD:%=props/prop_w_%.svg) \
	$(PROPS_2WILD:%=props/prop_w2_%.svg)
PNGS = $(SVGS:cards/%.svg=export/%.png) $(PROPS:props/%.svg=export/%.png)
V ?= 0
EXPORT = $(EXPORT_$(V))
EXPORT_0 = @echo "  EXPORT $<  "; inkscape -C -d 900 --export-png=$@ $< > /dev/null 2> /dev/null
EXPORT_1 = inkscape -C -d $(DPI) --export-png=$@ $<

PROP = $(PROP_$(V))
PROP_0 = @echo "  PROP $@  "; python3 $^ $* $@.tmp && mv $@.tmp $@
PROP_1 = python3 $^ $* $@.tmp && mv $@.tmp $@

.PHONY: all clean realclean genprops deck

all: export.pdf

deck: $(PNGS) cardset/.done

genprops: $(PROPS)

clean:
	rm -rf $(PNGS) $(PROPS)

realclean: clean
	rm Makefile

%/:
	mkdir $@

cardset/.done: scripts/deck.py cardset/ $(PNGS)
	python3 $< count.yaml export/ cardset/
	touch $@

.PRECIOUS: $(PROPS)
props/prop_n_%.svg: scripts/transform.py names.yaml templs/card_temp_prop.svg
	@mkdir -p props
	$(PROP)
props/prop_2_%.svg: scripts/transform.py names.yaml templs/card_temp_2prop.svg
	@mkdir -p props
	$(PROP)
props/prop_g_%.svg: scripts/transform.py names.yaml templs/card_temp_gprop.svg
	@mkdir -p props
	$(PROP)
props/prop_w_%.svg: scripts/transform.py names.yaml templs/card_temp_wprop.svg
	@mkdir -p props
	$(PROP)
props/prop_w2_%.svg: scripts/transform.py names.yaml templs/card_temp_wprop2.svg
	@mkdir -p props
	$(PROP)

export/%.png: cards/%.svg export/
	$(EXPORT)

export/%.png: props/%.svg export/
	$(EXPORT)

cards.csv: scripts/export_pc.py count.yaml export/ $(PNGS)
	python3 $< count.yaml export $@

export.tex: scripts/export.py count.yaml export/ $(PNGS)
	python3 $< count.yaml export $@

%.pdf: %.tex
	pdflatex $<
