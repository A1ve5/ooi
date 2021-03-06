# Copyright 2015 LIP - INDIGO-DataCloud
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

from ooi.occi.core import attribute as attr
from ooi.occi.core import kind
from ooi.occi.core import resource
from ooi.occi import helpers


class SecurityGroupResource(resource.Resource):
    attributes = attr.AttributeCollection({
        "occi.securitygroup.rules": attr.MutableAttribute(
            "occi.securitygroup.rules", description="Security Rules",
            attr_type=attr.AttributeType.list_type),
        "occi.securitygroup.state": attr.InmutableAttribute(
            "occi.securitygroup.state",
            description="Current state of the instance",
            attr_type=attr.AttributeType.string_type)
    })
    kind = kind.Kind(helpers.build_scheme('infrastructure'), 'securitygroup',
                     'securitygroup resource', attributes, 'securitygroup/',
                     parent=resource.Resource.kind
                     )

    def __init__(self, title, id=None, rules=None, summary=None,
                 state=None, mixins=[]):
        super(SecurityGroupResource, self).__init__(title, mixins,
                                                    summary=summary,
                                                    id=id)
        self.rules = rules
        self.attributes["occi.securitygroup.state"] = (
            attr.InmutableAttribute.from_attr(
                self.attributes["occi.securitygroup.state"], state))

    @property
    def rules(self):
        return self.attributes["occi.securitygroup.rules"].value

    @rules.setter
    def rules(self, value):
        self.attributes["occi.securitygroup.rules"].value = value

    @property
    def state(self):
        return self.attributes["occi.securitygroup.state"].value