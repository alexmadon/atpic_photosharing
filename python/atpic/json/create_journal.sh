# create journal template
# see http://edgeofsanity.net/article/2012/12/26/elasticsearch-for-logging.html
# Since we've decided to create an index a day, there's two ways to configure the mapping and features of each index. We can either create the indexes explicitly with the settings we want, or we can use a template such that any index created implicitly by writing data to it, has the features and configurations we want! Templates make the most sense in this case, you we'll create them on the now running cluster!
# http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/


# Admin Indices Templates

# Index templates allow to define templates that will automatically be applied to new indices created. The templates include both settings and mappings, and a simple pattern template that controls if the template will be applied to the index created. For example:
curl -XDELETE localhost:9200/_template/template_log
curl -XPUT localhost:9200/_template/template_log -d @schema_journal.json
curl -XGET "localhost:9200/_template/template_log?pretty=1"

curl -XPOST localhost:9200/log2013/journal/xxxx-yy-dddd-ffff -d '{"dir_0":"/user/1"}'
curl -GET localhost:9200/log2013/journal/xxxx-yy-dddd-ffff
# curl -GET localhost9200/{log2014,log2013,log2012}/journal/xxxx-yy-dddd-ffff?pretty=1
