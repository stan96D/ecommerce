from ecommerce_website.services.product_category_service.product_category_attribute_service import ProductCategoryAttributeService
from ecommerce_website.services.product_category_service.product_category_attribute_view_service import ProductCategoryAttributeViewService


class ProductCategoryAttributeViewHandler:

    def get_serialized_product_category_attribute_views(self):
        category_attributes = ProductCategoryAttributeService.get_all_active_product_category_attributes()
        category_attribute_view_service = ProductCategoryAttributeViewService()
        category_attribute_views = category_attribute_view_service.generate(
            category_attributes)
        serialized_category_attribute_views = [category_attribute_view.serialize(
        ) for category_attribute_view in category_attribute_views]
        combined = self.__combine(serialized_category_attribute_views)
        return combined
    
    def __combine(self, serialized_category_attribute_views):

        combined_data = {}

        for item in serialized_category_attribute_views:
            category_id = item['category_id']
            category_name = item['category_name']
            attribute_type_id = item['attribute_type_id']

            if category_id not in combined_data:
                combined_data[category_id] = {
                    'category_name': category_name,
                    'category_id': category_id,
                    'attributes': [{
                        'attribute_type_name': item['attribute_type_name'],
                        'attribute_type_id': attribute_type_id,
                        'product_attributes': [attr for attr in item['product_attributes'] if attr['id'] == attribute_type_id]
                    }]
                }
            else:
                category = combined_data[category_id]
                found = False
                for attribute in category['attributes']:
                    if attribute['attribute_type_id'] == attribute_type_id:
                        attribute['product_attributes'].extend([attr for attr in item['product_attributes'] if attr['id'] == attribute_type_id])
                        found = True
                        break
                if not found:
                    category['attributes'].append({
                        'attribute_type_name': item['attribute_type_name'],
                        'attribute_type_id': attribute_type_id,
                        'product_attributes': [attr for attr in item['product_attributes'] if attr['id'] == attribute_type_id]
                    })


        combined_category_attribute_views = list(combined_data.values())

        return combined_category_attribute_views

    
