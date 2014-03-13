# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ironic.common import exception
from ironic.drivers import base


def _raise_unsupported_error(method=None):
    if method:
        raise exception.UnsupportedDriverExtension(_(
            "Unsupported method (%s) passed through to vendor extension.")
            % method)
    raise exception.InvalidParameterValue(_(
        "Method not specified when calling vendor extension."))


class MixinVendorInterface(base.VendorInterface):
    """Wrapper around multiple VendorInterfaces."""

    def __init__(self, mapping):
        """Wrapper around multiple VendorInterfaces.

        :param mapping: dict of {'method': interface} specifying how to combine
                        multiple vendor interfaces into one vendor driver.

        """
        self.mapping = mapping

    def _map(self, **kwargs):
        method = kwargs.get('method')
        return self.mapping.get(method) or _raise_unsupported_error(method)

    def validate(self, *args, **kwargs):
        """Call validate on the appropriate interface only.

        :raises: UnsupportedDriverExtension if 'method' can not be mapped to
                 the supported interfaces.
        :raises: InvalidParameterValue if **kwargs does not contain 'method'.

        """
        route = self._map(**kwargs)
        route.validate(*args, **kwargs)

    def vendor_passthru(self, task, node, **kwargs):
        """Call vendor_passthru on the appropriate interface only.

        Returns or raises according to the requested vendor_passthru method.

        :raises: UnsupportedDriverExtension if 'method' can not be mapped to
                 the supported interfaces.
        :raises: InvalidParameterValue if **kwargs does not contain 'method'.

        """
        route = self._map(**kwargs)
        return route.vendor_passthru(task, node, **kwargs)
