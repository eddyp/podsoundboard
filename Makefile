GENBINS = ui_mainwindow.py

ui_mainwindow.py: mainwindow.ui
	pyside-uic $^ -o $@
	chmod +x $@

clean:
	rm -f $(GENBINS)
