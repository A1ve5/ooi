# Copyright 2015 Spanish National Research Council
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

import uuid

from ooi.occi.core import action
from ooi.occi.core import attribute
from ooi.occi.core import category
from ooi.occi.core import entity
from ooi.occi.core import kind
from ooi.occi.core import link
from ooi.occi.core import mixin
from ooi.occi.core import resource
from ooi.tests import base


class TestAttributes(base.TestCase):
    def test_base(self):
        attr = attribute.Attribute("occi.foo.bar", "bar")
        self.assertEqual("bar", attr.value)
        self.assertEqual("occi.foo.bar", attr.name)
        self.assertEqual(False, attr.required)
        self.assertEqual(None, attr.default)
        self.assertEqual(None, attr.description)

    def test_default_value(self):
        attr = attribute.Attribute("occi.foo.bar", default="bar")
        self.assertEqual(None, attr.value)
        self.assertEqual("bar", attr.default)

    def test_required(self):
        attr = attribute.Attribute("occi.foo.bar", required=True)
        self.assertEqual(True, attr.required)

    def test_description(self):
        attr = attribute.Attribute("occi.foo.bar", description="foo")
        self.assertEqual("foo", attr.description)

    def test_mutable(self):
        attr = attribute.MutableAttribute("occi.foo.bar", "bar")
        attr.value = "bazonk"
        self.assertEqual("bazonk", attr.value)
        self.assertEqual(attribute.AttributeType.object_type, attr.attr_type)

    def test_inmutable(self):
        attr = attribute.InmutableAttribute("occi.foo.bar", "bar")
        self.assertEqual(attribute.AttributeType.object_type, attr.attr_type)

        def set_val():
            attr.value = "bazonk"

        self.assertRaises(AttributeError, set_val)

    def test_attribute_type_list(self):
        l = attribute.AttributeType.list_type
        l.check_type([1])
        l.check_type(None)
        self.assertRaises(TypeError, l.check_type, 1)
        self.assertRaises(TypeError, l.check_type, {"a": "b"})
        self.assertRaises(TypeError, l.check_type, "foo")
        self.assertRaises(TypeError, l.check_type, True)

    def test_attribute_type_hash(self):
        h = attribute.AttributeType.hash_type
        h.check_type({})
        h.check_type(None)
        self.assertRaises(TypeError, h.check_type, 1)
        self.assertRaises(TypeError, h.check_type, [])
        self.assertRaises(TypeError, h.check_type, "foo")
        self.assertRaises(TypeError, h.check_type, True)

    def test_attribute_type_string(self):
        s = attribute.AttributeType.string_type
        s.check_type("hey")
        s.check_type(None)
        self.assertRaises(TypeError, s.check_type, 1)
        self.assertRaises(TypeError, s.check_type, [])
        self.assertRaises(TypeError, s.check_type, {})
        self.assertRaises(TypeError, s.check_type, True)

    def test_attribute_type_number(self):
        n = attribute.AttributeType.number_type
        n.check_type(1.0)
        n.check_type(None)
        self.assertRaises(TypeError, n.check_type, [])
        self.assertRaises(TypeError, n.check_type, {})
        self.assertRaises(TypeError, n.check_type, "foo")
        self.assertRaises(TypeError, n.check_type, True)

    def test_attribute_type_bool(self):
        b = attribute.AttributeType.boolean_type
        b.check_type(True)
        b.check_type(None)
        self.assertRaises(TypeError, b.check_type, 1)
        self.assertRaises(TypeError, b.check_type, [])
        self.assertRaises(TypeError, b.check_type, {})
        self.assertRaises(TypeError, b.check_type, "foo")

    def test_attribute_type_object(self):
        o = attribute.AttributeType.object_type
        o.check_type(None)
        o.check_type(1)
        o.check_type([])
        o.check_type({})
        o.check_type("foo")
        o.check_type(True)


class TestAttributeCollection(base.TestCase):
    def test_collection(self):
        col = attribute.AttributeCollection()
        self.assertEqual({}, col.attributes)

    def test_collection_raises_if_not_set(self):
        col = attribute.AttributeCollection(["foo"])
        self.assertRaises(AttributeError,
                          col.__getitem__,
                          "foo")

    def test_collection_from_seq(self):
        seq = ["foo", "bar"]
        col = attribute.AttributeCollection(seq)
        self.assertItemsEqual(seq, col.attributes.keys())

    def test_collection_from_map(self):
        mapping = {"foo": attribute.Attribute("occi.foo.bar", "crap")}
        col = attribute.AttributeCollection(mapping)
        self.assertEqual(mapping, col.attributes)

    def test_update(self):
        mapping1 = {"occi.foo.1": attribute.Attribute("occi.foo.1", "bar")}
        mapping2 = {"occi.foo.2": attribute.Attribute("occi.foo.2", "baz")}
        col1 = attribute.AttributeCollection(mapping1)
        col2 = attribute.AttributeCollection(mapping2)
        self.assertEqual(mapping1, col1.attributes)
        self.assertEqual(mapping2, col2.attributes)
        col1.update(col2)
        mapping1.update(mapping2)
        self.assertEqual(mapping1, col1.attributes)

    def test_update_invalid(self):
        mapping = {"occi.foo.1": attribute.Attribute("occi.foo.1", "bar")}
        col = attribute.AttributeCollection(mapping)
        self.assertRaises(TypeError,
                          col.update,
                          {"foo": "bar"})

    def test_collection_from_invalid_map(self):
        mapping = {"foo": "bar"}
        self.assertRaises(TypeError,
                          attribute.AttributeCollection,
                          mapping)

    def test_collection_from_invalid(self):
        mapping = 1
        self.assertRaises(TypeError,
                          attribute.AttributeCollection,
                          mapping)


class BaseTestCoreOCCICategory(base.TestCase):
    args = ("scheme", "term", "title")
    obj = category.Category

    def test_obj(self):
        cat = self.obj(*self.args)

        for i in self.args:
            self.assertEqual(i, getattr(cat, i))


class TestCoreOCCICategory(BaseTestCoreOCCICategory):
    pass


class TestCoreOCCIKind(BaseTestCoreOCCICategory):
    obj = kind.Kind

    def setUp(self):
        super(TestCoreOCCIKind, self).setUp()

    def test_obj(self):
        k = self.obj(*self.args)
        for i in (self.args):
            self.assertEqual(i, getattr(k, i))

    def test_actions(self):
        actions = [action.Action(None, None, None)]
        kind = self.obj(*self.args, actions=actions)

        for i in (self.args):
            self.assertEqual(i, getattr(kind, i))
        self.assertEqual(actions, kind.actions)

    def test_actions_empty(self):
        actions = []
        kind = self.obj(*self.args, actions=actions)

        for i in (self.args):
            self.assertEqual(i, getattr(kind, i))
        self.assertEqual(actions, kind.actions)

    def test_actions_invalid(self):
        actions = None
        self.assertRaises(TypeError,
                          self.obj,
                          *self.args,
                          actions=actions)

    def test_actions_invalid_list(self):
        actions = [None]
        self.assertRaises(TypeError,
                          self.obj,
                          *self.args,
                          actions=actions)


def TestCoreOCCIKindRelations(TestCoreOCCIKind):
    def test_parent(self):
        parent = self.obj(None, None, None)
        kind = self.obj(*self.args, parent=parent)

        for i in (self.args):
            self.assertEqual(i, getattr(kind, i))
        self.assertEqual(parent, kind.parent)

    def test_parent_invalid(self):
        parent = None
        self.assertRaises(TypeError,
                          self.obj,
                          *self.args,
                          parent=parent)


class TestCoreOCCIMixin(TestCoreOCCIKind):
    obj = mixin.Mixin

    def relation_test(self, relation, rel_type):
        rel = [rel_type(None, None, None)]
        kwargs = {relation: rel}
        o = self.obj(*self.args, **kwargs)

        for i in (self.args):
            self.assertEqual(i, getattr(o, i))
        self.assertEqual(rel, getattr(o, relation))

    def test_depends(self):
        self.relation_test("depends", mixin.Mixin)

    def test_applies(self):
        self.relation_test("applies", kind.Kind)

    def relation_invalid(self, relation):
        kwargs = {relation: None}
        self.assertRaises(TypeError,
                          self.obj,
                          *self.args,
                          **kwargs)


class TestCoreOCCIAction(BaseTestCoreOCCICategory):
    obj = action.Action


class TestCoreOCCIEntity(base.TestCase):
    def test_resource_class(self):
        e = entity.Entity
        self.assertIn("occi.core.id", e.attributes)
        self.assertIn("occi.core.title", e.attributes)
        self.assertIsNone(e.kind.parent)
        # TODO(aloga): We need to check that the attributes are actually set
        # after we get an object

    def test_entity(self):
        e = entity.Entity("bar", [])
        self.assertIsInstance(e.kind, kind.Kind)
        self.assertIn("occi.core.id", e.attributes)
        self.assertIn("occi.core.title", e.attributes)

        self.assertIs(e.id, e.attributes["occi.core.id"].value)

        def set_attr():
            e.attributes["occi.core.id"].value = "foo"
        self.assertRaises(AttributeError, set_attr)

        def set_attr_directly():
            e.id = "foo"
        self.assertRaises(AttributeError, set_attr_directly)

        e.title = "baz"
        self.assertEqual("baz", e.attributes["occi.core.title"].value)
        self.assertEqual("baz", e.title)
        self.assertIs(e.title, e.attributes["occi.core.title"].value)

        e.attributes["occi.core.title"].value = "bar"
        self.assertEqual("bar", e.attributes["occi.core.title"].value)
        self.assertEqual("bar", e.title)
        self.assertIs(e.title, e.attributes["occi.core.title"].value)

    def test_entities(self):
        e1 = entity.Entity("foo", [])
        e2 = entity.Entity("bar", [])
        self.assertNotEqual(e1.id, e2.id)


class TestCoreOCCIResource(base.TestCase):
    def test_resource_class(self):
        r = resource.Resource
        self.assertIn("occi.core.id", r.attributes)
        self.assertIn("occi.core.summary", r.attributes)
        self.assertIn("occi.core.title", r.attributes)
        self.assertEqual(entity.Entity.kind, r.kind.parent)
        # TODO(aloga): We need to check that the attributes are actually set
        # after we get an object

    def test_resource(self):
        id = uuid.uuid4().hex
        r = resource.Resource("bar", [], summary="baz", id=id)
        self.assertIsInstance(r.kind, kind.Kind)
        self.assertEqual("resource", r.kind.term)
        self.assertEqual("bar", r.title)
        self.assertEqual("baz", r.summary)
        self.assertEqual(id, r.id)
        self.assertEqual(entity.Entity.kind, r.kind.parent)
        r.summary = "bazonk"
        self.assertEqual("bazonk", r.summary)

    def test_resources_equal(self):
        id = uuid.uuid4().hex
        r = resource.Resource("bar", [], summary="baz", id=id)
        s = resource.Resource("bar", [], summary="baz", id=id)
        self.assertEqual(r, s)

    def test_valid_link(self):
        r1 = resource.Resource(None, [])
        r2 = resource.Resource(None, [])
        r1.link(r2)
        self.assertIsInstance(r1.links[0], link.Link)
        self.assertIs(r1, r1.links[0].source)
        self.assertIs(r2, r1.links[0].target)

    def test_mixins(self):
        m = mixin.Mixin(None, None, None)
        r = resource.Resource(None, [m])
        self.assertIsInstance(r.kind, kind.Kind)
        self.assertEqual([m], r.mixins)

    def test_invalid_mixins(self):
        self.assertRaises(TypeError,
                          resource.Resource,
                          None, ["foo"], None)


class TestCoreOCCILink(base.TestCase):
    def test_correct_link(self):
        resource_1 = resource.Resource(None, [], None)
        resource_2 = resource.Resource(None, [], None)
        resource_3 = resource.Resource(None, [], None)
        l = link.Link(None, [], resource_1, resource_2)
        self.assertIsInstance(l.kind, kind.Kind)
        self.assertEqual("link", l.kind.term)
        self.assertIs(resource_1, l.source)
        self.assertIs(resource_2, l.target)

        self.assertIs(resource_1, l.attributes["occi.core.source"].value)
        self.assertIs(resource_1, l.source)
        self.assertIs(resource_1, l.attributes["occi.core.source"].value)

        self.assertIs(resource_2, l.attributes["occi.core.target"].value)
        self.assertIs(resource_2, l.target)
        self.assertIs(resource_2, l.attributes["occi.core.target"].value)

        l.source = resource_3
        self.assertIs(resource_3, l.attributes["occi.core.source"].value)
        self.assertIs(resource_3, l.source)
        self.assertIs(resource_3, l.attributes["occi.core.source"].value)

        l.target = resource_1
        self.assertIs(resource_1, l.target)
        self.assertIs(resource_1, l.attributes["occi.core.target"].value)
