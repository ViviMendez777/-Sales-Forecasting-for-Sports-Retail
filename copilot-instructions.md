* empieza siempre tu respuesta con el emoji 🤖
* responde siempre en español
* recuerda que las variables del dataframe df que tienes que usar siempre en el codigo que generes son:
ventas_df: fecha', 'producto_id', 'nombre', 'categoria', 'subcategoria',
       'precio_base', 'es_estrella', 'unidades_vendidas', 'precio_venta',
       'ingresos',
       ...
       'subcategoria_h_Esterilla Yoga', 'subcategoria_h_Mancuernas Ajustables',
       'subcategoria_h_Mochila Trekking', 'subcategoria_h_Pesa Rusa',
       'subcategoria_h_Pesas Casa', 'subcategoria_h_Rodillera Yoga',
       'subcategoria_h_Ropa Montaña', 'subcategoria_h_Ropa Running',
       'subcategoria_h_Zapatillas Running', 'subcategoria_h_Zapatillas Trail'


competencia_df: ['fecha', 'producto_id', 'Amazon', 'Decathlon', 'Deporvillage']


'ingresos_expected', 'precio_competencia', 'ratio_precio',
       'nombre_h_Adidas Own The Run Jacket', 'nombre_h_Adidas Ultraboost 23',
       'nombre_h_Asics Gel Nimbus 25', 'nombre_h_Bowflex SelectTech 552',
       'nombre_h_Columbia Silver Ridge',
       'nombre_h_Decathlon Bandas Elásticas Set', 'nombre_h_Domyos BM900',
       'nombre_h_Domyos Kit Mancuernas 20kg',
       'nombre_h_Gaiam Premium Yoga Block', 'nombre_h_Liforme Yoga Pad',
       'nombre_h_Lotuscrafts Yoga Bolster', 'nombre_h_Manduka PRO Yoga Mat',
       'nombre_h_Merrell Moab 2 GTX',
       'nombre_h_New Balance Fresh Foam X 1080v12',
       'nombre_h_Nike Air Zoom Pegasus 40', 'nombre_h_Nike Dri-FIT Miler',
       'nombre_h_Puma Velocity Nitro 2', 'nombre_h_Quechua MH500',
       'nombre_h_Reebok Floatride Energy 5',
       'nombre_h_Reebok Professional Deck',
       'nombre_h_Salomon Speedcross 5 GTX', 'nombre_h_Sveltus Kettlebell 12kg',
       'nombre_h_The North Face Borealis', 'nombre_h_Trek Marlin 7',
       'categoria_h_Fitness', 'categoria_h_Outdoor', 'categoria_h_Running',
       'categoria_h_Wellness', 'subcategoria_h_Banco Gimnasio',
       'subcategoria_h_Bandas Elásticas', 'subcategoria_h_Bicicleta Montaña',
       'subcategoria_h_Bloque Yoga', 'subcategoria_h_Cojín Yoga',
       'subcategoria_h_Esterilla Fitness', 'subcategoria_h_Esterilla Yoga',
       'subcategoria_h_Mancuernas Ajustables',
       'subcategoria_h_Mochila Trekking', 'subcategoria_h_Pesa Rusa',
       'subcategoria_h_Pesas Casa', 'subcategoria_h_Rodillera Yoga',
       'subcategoria_h_Ropa Montaña', 'subcategoria_h_Ropa Running',
       'subcategoria_h_Zapatillas Running', 'subcategoria_h_Zapatillas Trail'],
      dtype='object')
competencia_df: ['fecha', 'producto_id', 'Amazon', 'Decathlon', 'Deporvillage'],
* no uses en tu codigo ninguna otra variable que no este en la lista anterior salvo que la hayas definido tu mismo en el codigo que generes
* no uses ninguna libreria que no sean estas: pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter, streamlit, holidays





df column:Index(['fecha', 'producto_id', 'nombre', 'categoria', 'subcategoria',
       'precio_base', 'es_estrella', 'unidades_vendidas', 'precio_venta',
       'ingresos', 'año', 'mes', 'dia_semana', 'dia_mes', 'es_fin_semana',
       'es_festivo', 'es_black_friday', 'es_cyber_monday', 'trimestre',
       'semana_año', 'es_dia_laborable', 'es_inicio_mes', 'es_fin_mes',
       'unidades_vendidas_lag1', 'unidades_vendidas_lag2',
       'unidades_vendidas_lag3', 'unidades_vendidas_lag4',
       'unidades_vendidas_lag5', 'unidades_vendidas_lag6',
       'unidades_vendidas_lag7', 'unidades_vendidas_ma7',
       'descuento_porcentaje', 'precio_competencia', 'ratio_precio',
       'nombre_h_Adidas Own The Run Jacket', 'nombre_h_Adidas Ultraboost 23',
       'nombre_h_Asics Gel Nimbus 25', 'nombre_h_Bowflex SelectTech 552',
       'nombre_h_Columbia Silver Ridge',
       'nombre_h_Decathlon Bandas Elásticas Set', 'nombre_h_Domyos BM900',
       'nombre_h_Domyos Kit Mancuernas 20kg',
       'nombre_h_Gaiam Premium Yoga Block', 'nombre_h_Liforme Yoga Pad',
       'nombre_h_Lotuscrafts Yoga Bolster', 'nombre_h_Manduka PRO Yoga Mat',
       'nombre_h_Merrell Moab 2 GTX',
       'nombre_h_New Balance Fresh Foam X 1080v12',
       'nombre_h_Nike Air Zoom Pegasus 40', 'nombre_h_Nike Dri-FIT Miler',
       'nombre_h_Puma Velocity Nitro 2', 'nombre_h_Quechua MH500',
       'nombre_h_Reebok Floatride Energy 5',
       'nombre_h_Reebok Professional Deck',
       'nombre_h_Salomon Speedcross 5 GTX', 'nombre_h_Sveltus Kettlebell 12kg',
       'nombre_h_The North Face Borealis', 'nombre_h_Trek Marlin 7',
       'categoria_h_Fitness', 'categoria_h_Outdoor', 'categoria_h_Running',
       'categoria_h_Wellness', 'subcategoria_h_Banco Gimnasio',
       'subcategoria_h_Bandas Elásticas', 'subcategoria_h_Bicicleta Montaña',
       'subcategoria_h_Bloque Yoga', 'subcategoria_h_Cojín Yoga',
       'subcategoria_h_Esterilla Fitness', 'subcategoria_h_Esterilla Yoga',
       'subcategoria_h_Mancuernas Ajustables',
       'subcategoria_h_Mochila Trekking', 'subcategoria_h_Pesa Rusa',
       'subcategoria_h_Pesas Casa', 'subcategoria_h_Rodillera Yoga',
       'subcategoria_h_Ropa Montaña', 'subcategoria_h_Ropa Running',
       'subcategoria_h_Zapatillas Running', 'subcategoria_h_Zapatillas Trail'],
      dtype='object')



      ## columnas desde forestcasting
(720, 71)
<DatetimeArray>
['2025-11-01 00:00:00', '2025-11-02 00:00:00', '2025-11-03 00:00:00',
 '2025-11-04 00:00:00', '2025-11-05 00:00:00', '2025-11-06 00:00:00',
 '2025-11-07 00:00:00', '2025-11-08 00:00:00', '2025-11-09 00:00:00',
 '2025-11-10 00:00:00', '2025-11-11 00:00:00', '2025-11-12 00:00:00',
 '2025-11-13 00:00:00', '2025-11-14 00:00:00', '2025-11-15 00:00:00',
 '2025-11-16 00:00:00', '2025-11-17 00:00:00', '2025-11-18 00:00:00',
 '2025-11-19 00:00:00', '2025-11-20 00:00:00', '2025-11-21 00:00:00',
 '2025-11-22 00:00:00', '2025-11-23 00:00:00', '2025-11-24 00:00:00',
 '2025-11-25 00:00:00', '2025-11-26 00:00:00', '2025-11-27 00:00:00',
 '2025-11-28 00:00:00', '2025-11-29 00:00:00', '2025-11-30 00:00:00']
Length: 30, dtype: datetime64[ns]
Index(['fecha', 'producto_id', 'nombre', 'categoria', 'subcategoria',
       'precio_base', 'es_estrella', 'unidades_vendidas', 'precio_venta',
       'ingresos', 'año', 'mes', 'dia_mes', 'dia_semana', 'es_fin_semana',
       'es_festivo', 'unidades_vendidas_lag1', 'unidades_vendidas_lag2',
       'unidades_vendidas_lag3', 'unidades_vendidas_lag4',
       'unidades_vendidas_lag5', 'unidades_vendidas_lag6',
       'unidades_vendidas_lag7', 'unidades_vendidas_ma7',
       'descuento_porcentaje', 'precio_competencia', 'ratio_precio',
       'nombre_h_Adidas Own The Run Jacket', 'nombre_h_Adidas Ultraboost 23',
       'nombre_h_Asics Gel Nimbus 25', 'nombre_h_Bowflex SelectTech 552',
       'nombre_h_Columbia Silver Ridge',
       'nombre_h_Decathlon Bandas Elásticas Set', 'nombre_h_Domyos BM900',
       'nombre_h_Domyos Kit Mancuernas 20kg',
       'nombre_h_Gaiam Premium Yoga Block', 'nombre_h_Liforme Yoga Pad',
       'nombre_h_Lotuscrafts Yoga Bolster', 'nombre_h_Manduka PRO Yoga Mat',
       'nombre_h_Merrell Moab 2 GTX',
       'nombre_h_New Balance Fresh Foam X 1080v12',
       'nombre_h_Nike Air Zoom Pegasus 40', 'nombre_h_Nike Dri-FIT Miler',
       'nombre_h_Puma Velocity Nitro 2', 'nombre_h_Quechua MH500',
       'nombre_h_Reebok Floatride Energy 5',
       'nombre_h_Reebok Professional Deck',
       'nombre_h_Salomon Speedcross 5 GTX', 'nombre_h_Sveltus Kettlebell 12kg',
       'nombre_h_The North Face Borealis', 'nombre_h_Trek Marlin 7',
       'categoria_h_Fitness', 'categoria_h_Outdoor', 'categoria_h_Running',
       'categoria_h_Wellness', 'subcategoria_h_Banco Gimnasio',
       'subcategoria_h_Bandas Elásticas', 'subcategoria_h_Bicicleta Montaña',
       'subcategoria_h_Bloque Yoga', 'subcategoria_h_Cojín Yoga',
       'subcategoria_h_Esterilla Fitness', 'subcategoria_h_Esterilla Yoga',
       'subcategoria_h_Mancuernas Ajustables',
       'subcategoria_h_Mochila Trekking', 'subcategoria_h_Pesa Rusa',
       'subcategoria_h_Pesas Casa', 'subcategoria_h_Rodillera Yoga',
       'subcategoria_h_Ropa Montaña', 'subcategoria_h_Ropa Running',
       'subcategoria_h_Zapatillas Running', 'subcategoria_h_Zapatillas Trail'],
      dtype='object'