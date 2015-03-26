# automake script for 'cryptmount'
# RW Penney, November 2005

AM_CPPFLAGS = -DCM_SYSCONF_DIR="\"$(CM_SYSCONF_DIR)\"" \
		-DCM_SYSRUN_DIR="\"$(CM_SYSRUN_DIR)\"" \
		-DCM_MODULE_DIR="\"$(pkglibdir)\""

ACLOCAL_AMFLAGS = #-I m4
bin_PROGRAMS=cryptmount
cryptmount_SOURCES=cryptmount.c cryptmount.h \
	armour.c armour.h \
	armour-builtin.c armour-gcry.c armour-luks.c \
	blowfish.c blowfish.h \
	dmutils.c dmutils.h \
	fsutils.c fsutils.h \
	looputils.c looputils.h \
	tables.c tables.h \
	utils.c utils.h \
	cmtesting.c cmtesting.h
cryptmount_NONHEADERS = $(shell echo "${cryptmount_SOURCES}" | sed 's%\<[^ ]*\.h\>%%g')

if BUILD_LUKSCOMPAT
if !BUILD_MODULES
cryptmount_LDADD = ${libcryptsetup_LIBS}
endif
endif

localedir=$(datadir)/locale
INCLUDES=-DLOCALEDIR=\"$(localedir)\"
EXTRA_DIST = config.rpath mkinstalldirs cmtab.example \
	README.OpenSSL RELNOTES ToDo cryptmount.spec \
	debian/changelog debian/compat debian/control debian/copyright \
	debian/dirs debian/docs debian/rules debian/lintian-override \
	debian/postinst debian/postrm debian/watch debian/source/format

SUBDIRS = man po sysinit testing


#
# Build-information for dynamically-loadable key-manager modules
# (Dependent on gcc-compatible compiler, because libtool would be overkill)
#
MODULE_GENSRCS = utils.c
MODULE_GENHDRS = armour.h config.h utils.h
cm-gcry.so:	armour-gcry.c ${MODULE_GENSRCS} ${MODULE_GENHDRS}
	${CC} ${DEFS} -DAS_MODULE ${DEFAULT_INCLUDES} ${INCLUDES} \
		${AM_CPPFLAGS} ${CPPFLAGS} ${AM_CFLAGS} ${CFLAGS} \
		-shared -fPIC armour-gcry.c ${MODULE_GENSRCS} \
		${LIBS_GCRY} ${LDFLAGS} -o $@
cm-luks.so:	armour-luks.c ${MODULE_GENSRCS} ${MODULE_GENHDRS} looputils.c
	${CC} ${DEFS} -DAS_MODULE ${DEFAULT_INCLUDES} ${INCLUDES} \
		${AM_CPPFLAGS} ${CPPFLAGS} ${AM_CFLAGS} ${CFLAGS} \
		-shared -fPIC armour-luks.c ${MODULE_GENSRCS} \
		dmutils.c looputils.c ${LIBS_LUKS} ${LDFLAGS} -o $@
all:	${CM_MODULES}

install-exec-hook:	install-etcdir install-modules
	chown root.root $(DESTDIR)$(bindir)/cryptmount$(EXEEXT)
	chmod u+srwx,go-w,go+r $(DESTDIR)$(bindir)/cryptmount$(EXEEXT)
	@if test -z "$(DESTDIR)" -o "$(DESTDIR)" = "/"; then \
		modprobe -a loop dm-crypt || true; \
		( egrep -q '\<device-mapper\>' /proc/devices \
			&& egrep -q '\<loop\>' /proc/devices ) || \
		echo "Warning: kernel support for /dev/loop and /dev/mapper is needed by cryptmount"; \
	fi


.PHONY:	install-etcdir
install-etcdir:
	if test ! -d "${DESTDIR}${CM_SYSCONF_DIR}" ; then \
	    ${mkdir_p} "${DESTDIR}${CM_SYSCONF_DIR}" ; \
	    ${INSTALL_PROGRAM_ENV} ${INSTALL_DATA} cmtab.example "${DESTDIR}${CM_SYSCONF_DIR}" ; \
	fi
	if test ! -f "${DESTDIR}${CM_SYSCONF_DIR}/cmtab" ; then \
	    echo -e "# ${CM_SYSCONF_DIR}/cmtab - encrypted filesystem information for cryptmount\n# try 'man 8 cryptmount' or 'man 5 cmtab' for more details\n" >> "${DESTDIR}${CM_SYSCONF_DIR}/cmtab"; \
	fi


install-modules:	${CM_MODULES}
	test -z "${CM_MODULES}" -o -d "${DESTDIR}${pkglibdir}" || ${mkdir_p} "${DESTDIR}${pkglibdir}"
	for mod in ${CM_MODULES}; do \
		${INSTALL_PROGRAM_ENV} ${INSTALL_PROGRAM} -m 700 $${mod} "${DESTDIR}${pkglibdir}"; \
		chown root.root ${DESTDIR}${pkglibdir}/$${mod}; \
	done


install-setup:	setupscript
	test -d "${DESTDIR}${sbindir}" || ${mkdir_p} "${DESTDIR}${sbindir}"
	${INSTALL_PROGRAM_ENV} ${INSTALL_SCRIPT} setupscript "${DESTDIR}${sbindir}/cryptmount-setup"


clean-local:
	-rm -f ${CM_MODULES}
	-rm -f splint.log

dist-hook:
	sed -e "s,^\(Version:\s*\)[0-9].*,\1${VERSION}," cryptmount.spec > cm_spec.new; cmp -q cryptmount.spec cm_spec.new || mv cm_spec.new cryptmount.spec; rm -f cm_spec.new

pedantic:	CFLAGS = -Wall -W -pedantic -g
pedantic:	${bin_PROGRAMS} ${CM_MODULES}

if HAVE_DOXYGEN
doxydocs:	doxygen.conf
	doxygen doxygen.conf
endif

.PHONY:	splint
splint:
	@echo -n "" > splint.log
	for src in ${cryptmount_NONHEADERS}; do \
		echo "==== $${src} ====" >> splint.log; \
		splint ${DEFS} ${DEFAULT_INCLUDES} ${INCLUDES} ${AM_CPFLAGS} ${CPPFLAGS} -D__signed__="" -posix-lib -checks $${src} >> splint.log 2>&1 ; \
		echo -e "\n\n" >> splint.log || true; \
	done

# 'cmtest' target is for use with 'mudslinger' testing script:
cmtest:	CFLAGS = -Wall -g -DTESTING -DCM_SRCDIR=\"${abs_srcdir}\"
cmtest:	${bin_PROGRAMS} ${CM_MODULES}
	${MAKE} -C testing autokeys mudslinger


.PHONY:	depend
depend:
	${CC} -MM ${DEFS} ${DEFAULT_INCLUDES} ${INCLUDES} ${AM_CPFLAGS} ${CPPFLAGS} ${cryptmount_NONHEADERS} > .depend
-include .depend
