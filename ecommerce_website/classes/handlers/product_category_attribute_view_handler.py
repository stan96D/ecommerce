# from ecommerce_website.services.product_category_service.product_category_attribute_service import ProductCategoryAttributeService
# from ecommerce_website.services.product_category_service.product_category_attribute_view_service import ProductCategoryAttributeViewService


# class ProductCategoryAttributeViewHandler:

#     def get_serialized_product_category_attribute_views(self):
#         category_attributes = ProductCategoryAttributeService.get_all_active_product_category_attributes()
#         category_attribute_view_service = ProductCategoryAttributeViewService()
#         category_attribute_views = category_attribute_view_service.generate(
#             category_attributes)
#         serialized_category_attribute_views = [category_attribute_view.serialize(
#         ) for category_attribute_view in category_attribute_views]
#         combined = self.__combine(serialized_category_attribute_views)
#         return combined
    

#     def __combine(self, serialized_category_attribute_views):
#         combined = {}
#         for entry in serialized_category_attribute_views:
#             category_id = entry['category_id']
#             if category_id not in combined:
#                 combined[category_id] = {
#                     'category_name': entry['category_name'],
#                     'category_id': category_id,
#                     'attribute_types': {}
#                 }
            
#             attribute_types = combined[category_id]['attribute_types']
#             attribute_type_id = entry['attribute_type_id']
#             attribute_type_name = entry['attribute_type_name']
#             product_attributes = entry['product_attributes']
            
#             if attribute_type_id not in attribute_types:
#                 attribute_types[attribute_type_id] = {
#                     'attribute_type_name': attribute_type_name,
#                     'product_attributes': []
#                 }
            
#             attribute_types[attribute_type_id]['product_attributes'].extend(product_attributes)
        
#         combined_entries = []
#         for category_id, category_data in combined.items():
#             combined_entries.append({
#                 'category_name': category_data['category_name'],
#                 'category_id': category_id,
#                 'attribute_types': list(category_data['attribute_types'].values())
#             })
#         print(combined_entries)
#         return combined_entries




    
