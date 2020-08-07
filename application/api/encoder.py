from connexion.apps.flask_app import FlaskJSONEncoder
import six

from .models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            attr_dict = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                attr_dict[attr] = value
            return attr_dict
        return FlaskJSONEncoder.default(self, o)
