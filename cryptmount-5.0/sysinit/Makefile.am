# automake script for cryptmount system-startup mechanisms
# RW Penney, April 2013

EXTRA_DIST = cryptmount.service.in modules-load.conf \
	setupscript.sh.in initscript.in

scripttransform='s,@EXENAME@,$(bindir)/cryptmount$(EXEEXT),g; \
		s,@SYSCONF_DIR@,$(CM_SYSCONF_DIR),g; \
		s,@PKG_NAME@,$(PACKAGE_NAME),g; \
		s,@PKG_VERSION@,$(VERSION),g; \
		s,@LCL_DIR@,$(localedir),g'


initscript:	initscript.in
	sed ${scripttransform} $< > $@

cryptmount.service:	cryptmount.service.in
	sed ${scripttransform} $< > $@

setupscript:	setupscript.sh.in
	sed ${scripttransform} $< > $@


install-exec-hook:	install-inits install-setup


install-inits:	cryptmount.service initscript
if USE_SYSTEMD
	test -d "${DESTDIR}/usr/lib/systemd/system" || mkdir -p "${DESTDIR}/usr/lib/systemd/system"
	test -d "${DESTDIR}/etc/modules-load.d" || mkdir -p "${DESTDIR}/etc/modules-load.d"
endif	# USE_SYSTEMD
	if test -d "${DESTDIR}/usr/lib/systemd/system" ; then \
	    ${INSTALL_PROGRAM_ENV} ${INSTALL_DATA} cryptmount.service "${DESTDIR}/usr/lib/systemd/system"; \
	fi
	if test -d "${DESTDIR}/etc/modules-load.d" ; then \
	     ${INSTALL_PROGRAM_ENV} ${INSTALL_DATA} modules-load.conf "${DESTDIR}/etc/modules-load.d/cryptmount.conf"; \
	fi
if !USE_SYSTEMD
	if test -d "${DESTDIR}/etc/init.d" ; then \
	    ${INSTALL_PROGRAM_ENV} ${INSTALL_SCRIPT} initscript "${DESTDIR}/etc/init.d/cryptmount" ; \
	fi
endif	# !USE_SYSTEMD


install-setup:	setupscript
	test -d "${DESTDIR}${sbindir}" || ${mkdir_p} "${DESTDIR}${sbindir}"
	${INSTALL_PROGRAM_ENV} ${INSTALL_SCRIPT} setupscript "${DESTDIR}${sbindir}/cryptmount-setup"


clean-local:
	-rm -f cryptmount.service initscript setupscript
