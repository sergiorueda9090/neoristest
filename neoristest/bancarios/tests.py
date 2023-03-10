from django.test import TestCase
from . import views
from django.urls import reverse

# Create your tests here.
class ListViewTest(TestCase):
    #Redirect template
    def test_view_url_exists_at_desired_location(self):
        resp_home = self.client.get('/')
        self.assertEqual(resp_home.status_code, 200)
    
    #template
    def test_view_uses_correct_template(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'bancarios/base.html')
    
    #Listar el JSON
    def test_lists_all_register(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['cantidadTitulos'] > 0)
        self.assertTrue( len(resp.context['productos']) > 0)

    #Buscar registro
    def test_buscar_register(self):
        resp = self.client.get('/')
        for productitem in resp.context["productos"]:
            #print(productitem["idTitulo"])
            self.assertEqual(productitem["idTitulo"], "USD")
        self.assertEqual(resp.status_code, 200)

    #Actualizar Fecha
    def test_buscar_register(self):
        resp = self.client.get('/')
        self.assertEqual(resp.context["productos"][0]["idTitulo"], "USD")
        resp.context["productos"][0]["fecha_creacion"] = "2022-02-01"

    #Redireccion de metodos
    def test_redireccion_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'bancarios/base.html')
        self.assertRedirects(resp, '/')



 

