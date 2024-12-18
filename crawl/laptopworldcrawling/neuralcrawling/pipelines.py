# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NeuralcrawlingPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        #Strip all white space from the string
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'manufacturer':
                manu_list = ['Asus', 'HP', 'Dell', 'Lenovo', 'LG', 'ASUS', 'Acer', 'MSI', 'Gigabyte', 'Stealth', 'Creator', 'Aspire']
                values = adapter.get(field_name).split(' ')
                for value in values:
                    if value in manu_list:
                        if value == 'Stealth' or value == 'Creator':
                            value = 'MSI'
                        if value == 'Aspire':
                            value = 'Acer'
                        adapter[field_name] = value
                        break

            elif field_name == 'cpu_manufacturer':
                value = adapter.get(field_name)[0]
                if value == 'Intel®' or value == 'Intel':
                    adapter[field_name] = 'Intel'
                elif value == 'AMD' or value == 'Snapdragon':
                    adapter[field_name] = value

            elif field_name == 'cpu_brand_modifier':
                value = adapter.get(field_name)
                if value[0] == 'Intel®' or value[0] == 'Intel':
                    if value[2][0] == 'i':
                        adapter[field_name] = value[2].split('-')[0]
                    elif value[2] == 'Ultra':
                        adapter[field_name] = value[2]+value[3]
                    else:
                        adapter[field_name] = value[2]
                elif value[0] == 'AMD':
                    if value[2] == 'AI':
                        adapter[field_name] = value[2]+value[3]
                    else:
                        adapter[field_name] = value[2].split('-')[0]
                elif value[0] == 'Snapdragon':
                    adapter[field_name] = value[2]+value[3]

            elif field_name == 'cpu_generation':
                values = adapter.get(field_name)
                v = ''
                for value in values:
                    if value[len(value)-1] == 'H' or value[len(value)-1] == 'U' or value[len(value)-1] == 'P' or value[len(value)-1] == 'S' or value[len(value)-1] == 'V' or value[len(value)-1] == 'E' or value[len(value)-2] == 'G' or value[len(value)-1] == 'X':
                        v = value
                        break
                if '-' in v:
                    adapter[field_name] = v.split('-')[1]
                else:
                    adapter[field_name] = v

            elif field_name == 'cpu_speed':
                value = adapter.get(field_name)
                index = value.index('to')
                adapter[field_name] = value[index+1]

            elif field_name == 'ram':
                value = adapter.get(field_name).split(' ')
                adapter[field_name] = value[0]

            elif field_name == 'ram_type':
                values = adapter.get(field_name).split(' ')
                v = ''
                for value in values:
                    if value[0] == 'D' or value[0] == 'L':
                        v = value
                        break
                if '-' in v:
                    adapter[field_name] = v.split('-')[0]
                else:
                    adapter[field_name] = v

            elif field_name == 'bus':
                values = adapter.get(field_name).split(' ')
                v = ''
                for value in values:
                    if len(value) > 3 and value[len(value)-3:] == 'MHz':
                        v = value
                        break
                    else:
                        v = ''
                if '-' in v:
                    adapter[field_name] = v.split('-')[1]
                else:
                    adapter[field_name] = v   

            elif field_name == 'storage':
                value = adapter.get(field_name).split(' ')
                adapter[field_name] = value[0]
            
            elif field_name == 'screen_size':
                value = adapter.get(field_name).split(' ')
                adapter[field_name] = value[0].replace('inch', '')

            elif field_name == 'screen_resolution':
                value = adapter.get(field_name)
                value = value.split('(')[1]
                value = value.split(')')[0]
                adapter[field_name] = value
            
            elif field_name == 'gpu_manufacturer':
                value = adapter.get(field_name).split(' ')
                adapter[field_name] = value[0]

            elif field_name == 'weight':
                value = adapter.get(field_name)
                adapter[field_name] = value

            elif field_name == 'battery':
                value = adapter.get(field_name).split(' ')
                if len(value) > 1:
                    adapter[field_name] = value[1]
                else:
                    adapter[field_name] = value[0]
            
            elif field_name == 'price':
                value = adapter.get(field_name).split(' ')
                adapter[field_name] = value[0]
                
        return item
