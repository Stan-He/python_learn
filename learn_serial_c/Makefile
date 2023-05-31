NAME          := serial-demo
.DEFAULT_GOAL := ${NAME}



BUILD-DIR     := .build
${BUILD-DIR}:

${BUILD-DIR}:
	meson  $@
	@echo "Configuration located in: $@"
	@echo "-------------------------------------------------------"

.PHONY: ${NAME}
${NAME}: ${BUILD-DIR}
	ninja -C ${BUILD-DIR}



.PHONY: clean
clean:
ifneq ("$(wildcard ${BUILD-DIR})","")
	ninja -C ${BUILD-DIR} -t $@
endif

.PHONY: purge
purge:
ifneq ("$(wildcard ${BUILD-DIR})","")
	rm -rf ${BUILD-DIR}
endif
