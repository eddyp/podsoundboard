WIDGETS = mainwindow soundcontrol
GENBINS = $(foreach W, $(WIDGETS), ui_$(W).py)

#ui_mainwindow.py ui_soundcontrol.py

all: $(GENBINS)

ui_%.py: %.ui
	pyside-uic $^ -o $@

clean:
	rm -f $(GENBINS)

.PHONY: all clean
