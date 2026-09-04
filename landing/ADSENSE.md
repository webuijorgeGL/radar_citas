# Configuración de Google AdSense

La página contiene un conector global y tres ubicaciones preparadas para anuncios. Busca `ADSENSE:` en `../index.html` para encontrarlas rápidamente.

## 1. Conector global

Pega el script global entregado por AdSense en el bloque `ADSENSE: CONECTOR GLOBAL`, dentro de `<head>`. Solo debe existir una copia de este script en la página.

## 2. Unidades publicitarias

Crea tres unidades de anuncio responsive en AdSense y pega cada bloque `<ins class="adsbygoogle">` en su ubicación correspondiente:

- `PLACEMENT 1`: banner superior, antes del contenido principal.
- `PLACEMENT 2`: anuncio intermedio, después de la explicación del radar.
- `PLACEMENT 3`: banner inferior, antes del llamado final a Telegram.

Cada unidad normalmente también requiere esta inicialización inmediatamente después del elemento `<ins>`:

```html
<script>
  (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

Reemplaza el texto `Espacio para anuncio`; no pongas el anuncio dentro de `.ad-slot` si el código suministrado por AdSense requiere controlar directamente su propio tamaño. Puedes conservar `.ad-section` y la etiqueta `Publicidad`.

## Recomendaciones

- No invites a los usuarios a hacer clic en los anuncios.
- No confundas los anuncios con botones, navegación o mensajes de la DIAN.
- No coloques anuncios dentro de los enlaces a Telegram o a la DIAN.
- Publica las páginas de privacidad y contacto requeridas antes de solicitar aprobación a AdSense.
- Sustituye siempre `ca-pub-XXXXXXXXXXXXXXXX` y los identificadores de ejemplo por los valores reales de tu cuenta.
