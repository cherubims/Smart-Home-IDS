from rest_framework import serializers
from .models import NetworkTraffic

class NetworkTrafficSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """
        Convert `yes` / `no` or boolean values to boolean for `attack` field.
        """
        if 'attack' in data:
            if isinstance(data['attack'], bool):
                # No conversion needed if it's already a boolean
                pass
            elif isinstance(data['attack'], str):
                if data['attack'].lower() == 'yes':
                    data['attack'] = True
                elif data['attack'].lower() == 'no':
                    data['attack'] = False
                else:
                    raise serializers.ValidationError({
                        'attack': "Value must be 'yes', 'no', True, or False."
                    })
            else:
                raise serializers.ValidationError({
                    'attack': "Invalid data type for 'attack'. Must be a string or boolean."
                })
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Convert boolean values for `attack` back to `yes` / `no` when serializing.
        """
        ret = super().to_representation(instance)
        ret['attack'] = "yes" if instance.attack else "no"
        return ret

    class Meta:
        model = NetworkTraffic
        fields = '__all__'


















# from rest_framework import serializers
# from .models import NetworkTraffic

# class NetworkTrafficSerializer(serializers.ModelSerializer):
#     def to_internal_value(self, data):
#         """
#         Convert `yes` / `no` to boolean for `attack` field.
#         """
#         if 'attack' in data:
#             if data['attack'].lower() == 'yes':
#                 data['attack'] = True
#             elif data['attack'].lower() == 'no':
#                 data['attack'] = False
#             else:
#                 raise serializers.ValidationError({
#                     'attack': "Value must be 'yes' or 'no'."
#                 })
#         return super().to_internal_value(data)

#     def to_representation(self, instance):
#         """
#         Convert boolean values for `attack` back to `yes` / `no` when serializing.
#         """
#         ret = super().to_representation(instance)
#         ret['attack'] = "yes" if instance.attack else "no"
#         return ret

#     class Meta:
#         model = NetworkTraffic
#         fields = '__all__'
