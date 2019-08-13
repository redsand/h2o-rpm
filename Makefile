.PHONY:	rpm clean

H2O_VERSION ?= 3.26.0
H2O_RELEASE ?= 4765
INT_VERSION ?= 21000
VERSION = $(shell echo $(H2O_VERSION) | sed "s/-/_/")
BUILD_NUMBER ?= 1
TARBALL_NAME = h2o-$(H2O_VERSION).${H2O_RELEASE}
TARBALL = $(TARBALL_NAME).tar.gz
TARBALL_URL = https://h2o-release.s3.amazonaws.com/h2o/master/${H2O_RELEASE}/h2o-${H2O_VERSION}.${H2O_RELEASE}.zip
TOPDIR = /tmp/h2o-rpm
PWD = $(shell pwd)

rpm:
	@wget "${TARBALL_URL}" -O ${TARBALL}
	@rpmbuild -v -bb \
			--define "version $(VERSION)" \
			--define "int_version $(INT_VERSION)" \
			--define "h2o_version $(H2O_VERSION)" \
			--define "h2o_release $(H2O_RELEASE)" \
			--define "build_number $(BUILD_NUMBER)" \
			--define "tarball $(TARBALL)" \
			--define "tarball_name $(TARBALL_NAME)" \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			h2o.spec

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(TARBALL)

$(TARBALL):
	@spectool \
			--define "version $(VERSION)" \
			--define "int_version $(INT_VERSION)" \
			--define "h2o_version $(H2O_VERSION)" \
			--define "h2o_release $(H2O_RELEASE)" \
			--define "tarball $(TARBALL)" \
			-g h2o.spec

