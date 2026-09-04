# Configuración de unidades de Google AdSense

La página utiliza cinco ubicaciones manuales: tres unidades gráficas responsive y dos unidades Multiplex responsive. Busca `ADSENSE DISPLAY` y `ADSENSE MULTIPLEX` en `../index.html` para encontrarlas.

## 1. Conector global

El script global ya está instalado dentro de `<head>` y debe existir una sola vez. No lo repitas al insertar las unidades.

## Unidades gráficas

Crea tres unidades de tipo **Anuncios gráficos** con tamaño responsive. Copia cada código en `ADSENSE DISPLAY 1`, `2` y `3`, sustituyendo completamente el elemento `.ad-placeholder` de esa ubicación.

## Unidades Multiplex

Crea dos unidades de tipo **Anuncios Multiplex** con diseño responsive. Copia cada código en `ADSENSE MULTIPLEX 1` y `2`, sustituyendo completamente el elemento `.ad-placeholder` correspondiente.

Cada bloque debe conservar el `<ins class="adsbygoogle">` y su inicialización:

```html
<script>
  (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

## Recomendaciones

- Desactiva Auto ads en AdSense para evitar anuncios adicionales fuera de estas ubicaciones.
- No invites a los usuarios a hacer clic en los anuncios.
- No confundas los anuncios con botones, navegación o mensajes de la DIAN.
- No coloques anuncios dentro de los enlaces a Telegram o a la DIAN.
- Publica las páginas de privacidad y contacto requeridas antes de solicitar aprobación a AdSense.
- Sustituye siempre `ca-pub-XXXXXXXXXXXXXXXX` y los identificadores de ejemplo por los valores reales de tu cuenta.
