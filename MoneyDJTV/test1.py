from django.template import Template,Context

tf = open('C:\\Develop\\JustASK\\JustASK\\MoneyDJTV\\test.html', 'r')

temp_string = tf.read()
t = Template(temp_string)
c = Context({'my_name': 'Daryl Spitzer'})
result=t.render(c)

f = open('work.html', 'w')
f.write(result)
f.close()