OPTDIR := opt
SHAREDIR := usr/share

all:
	@echo Building is not required for this package.

install:
	mkdir -p ${DESTDIR}/${OPTDIR}
	cp -r kmeldb-ui ${DESTDIR}/${OPTDIR}
	mkdir -p ${DESTDIR}/${SHAREDIR}/applications
	cp com.github.vsvyatski.kmeldb-ui.desktop ${DESTDIR}/${SHAREDIR}/applications
