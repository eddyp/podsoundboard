WIDGETS := $(subst .ui,,$(wildcard *.ui))
GENBINS := $(foreach W, $(WIDGETS), ui_$(W).py)
PROG    := mainwindow.py

#ui_mainwindow.py ui_soundcontrol.py

all: $(GENBINS)

ui_%.py: %.ui
	pyside-uic $^ -o $@

run: $(GENBINS)
	python $(PROG)

clean:
	rm -f $(GENBINS) *.pyc

test:
	py.test

.PHONY: all clean run test
