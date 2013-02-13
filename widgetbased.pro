#-------------------------------------------------
#
# Project created by QtCreator 2013-02-02T00:54:00
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = widgetbased
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui \
    soundcontrol.ui \
    confsound.ui \
    filebrowse.ui

OTHER_FILES += \
    qsoundcontrol.py \
    mainwindow.py
