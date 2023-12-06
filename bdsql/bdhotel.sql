-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2023 a las 19:12:11
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bdhotel`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `idcliente` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `nacionalidad` varchar(50) NOT NULL,
  `celular` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `fnacimiento` varchar(50) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`idcliente`, `nombre`, `nacionalidad`, `celular`, `email`, `fnacimiento`, `borrado`) VALUES
('1115802400', 'OSCAR MARIN', 'Colombia', '3186024848', 'oscarm@gmail.com', '2000-02-15', 0),
('38879331', 'LUZ ADRIANA HERRERA ', 'Colombia', '3184335003', 'adrianahc2@gmail.com', '1976-08-27', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comandas`
--

CREATE TABLE `comandas` (
  `idcomanda` int(10) NOT NULL,
  `idcodigo` varchar(20) NOT NULL,
  `descripItem` varchar(30) NOT NULL,
  `idregistro` varchar(20) NOT NULL,
  `idcliente` varchar(30) NOT NULL,
  `idhabitacion` varchar(10) NOT NULL,
  `fecha` date NOT NULL,
  `cantidad` int(10) NOT NULL,
  `valor` int(10) NOT NULL,
  `subtotal` int(10) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `borrado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comandas`
--

INSERT INTO `comandas` (`idcomanda`, `idcodigo`, `descripItem`, `idregistro`, `idcliente`, `idhabitacion`, `fecha`, `cantidad`, `valor`, `subtotal`, `estado`, `foto`, `borrado`) VALUES
(1, 'PRODUCTO', 'CAFE MOLIDO', '1', '38879331', '101', '2023-12-07', 1, 5000, 5000, 'Por pagar', 'E20231206122941', 0),
(2, 'SERVICIO', 'LIMPIEZA CUARTO', '1', '38879331', '101', '2023-12-07', 1, 15000, 15000, 'Por pagar', 'E20231206123036', 0),
(3, 'PRODUCTO', 'PASEO ECOLOGICO', '2', '1115802400', '102', '2023-12-03', 1, 35000, 35000, 'Por pagar', 'E20231206124337', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comunicaciones`
--

CREATE TABLE `comunicaciones` (
  `Idcomunicacion` int(14) NOT NULL,
  `idcliente` int(15) NOT NULL,
  `fecha` date NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comunicaciones`
--

INSERT INTO `comunicaciones` (`Idcomunicacion`, `idcliente`, `fecha`, `tipo`, `descripcion`, `estado`, `borrado`) VALUES
(1, 38879331, '2023-11-22', 'SUGERENCIA', 'Recibir a los pasajeros', 'PENDIENTE', 0),
(2, 296305420, '2023-11-17', 'RECOMENDACION', 'Por favor mantener jabón en los baños. ', 'EN PROCESO', 0),
(3, 75623102, '2023-11-30', 'SUGERENCIA', 'Por favor guardar las maletas con cuidado', 'EN PROCESO', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `idFactura` int(10) NOT NULL,
  `idRegistro` int(10) NOT NULL,
  `idCliente` int(10) NOT NULL,
  `idcomanda` int(10) NOT NULL,
  `fecha` date NOT NULL,
  `total` int(10) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`idFactura`, `idRegistro`, `idCliente`, `idcomanda`, `fecha`, `total`, `borrado`) VALUES
(1567, 4725, 38879331, 13663, '2023-12-04', 380000, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gest_alqui`
--

CREATE TABLE `gest_alqui` (
  `id_alqui` int(4) NOT NULL,
  `placa` varchar(6) NOT NULL,
  `id_registro` int(11) NOT NULL,
  `num_licencia` varchar(15) NOT NULL,
  `fech_alqui` date NOT NULL,
  `fech_devo` date NOT NULL,
  `id_comanda` varchar(6) NOT NULL,
  `comentario` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gest_alqui`
--

INSERT INTO `gest_alqui` (`id_alqui`, `placa`, `id_registro`, `num_licencia`, `fech_alqui`, `fech_devo`, `id_comanda`, `comentario`) VALUES
(1, 'TPS001', 2, '123', '2023-12-04', '2023-12-04', '1', 'Prueba de comentario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gest_vehic`
--

CREATE TABLE `gest_vehic` (
  `id_placa` varchar(6) NOT NULL,
  `tipo` varchar(5) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `num_ocupa` varchar(2) NOT NULL,
  `estado` varchar(14) NOT NULL,
  `consumo` varchar(10) NOT NULL,
  `soat` date NOT NULL,
  `tecno_mec` date NOT NULL,
  `permiso` date NOT NULL,
  `kilometraje` int(11) NOT NULL,
  `img` varchar(50) NOT NULL,
  `precio` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gest_vehic`
--

INSERT INTO `gest_vehic` (`id_placa`, `tipo`, `marca`, `num_ocupa`, `estado`, `consumo`, `soat`, `tecno_mec`, `permiso`, `kilometraje`, `img`, `precio`) VALUES
('TPS001', 'MOTO', 'Yamaha Grizzly', '2', 'DISPONIBLE', '19.7 KM/L', '2023-12-31', '2023-12-31', '2023-12-31', 10000, '', 140000),
('TPS002', 'CARRO', 'Yamaha Rhino', '2', 'DISPONIBLE', '65 KM/L', '2023-12-31', '2023-12-31', '2023-12-31', 40000, '', 200000),
('TPS003', 'CARRO', 'Can Am Maverick Sport', '4', 'DISPONIBLE', '14.5 km/l', '2023-12-31', '2023-12-31', '2023-12-31', 5000, '', 280000),
('TPS004', 'CARRO', 'CAN AM', '4', 'DISPONIBLE', '23,53 km/l', '2023-12-31', '2023-12-31', '2023-12-31', 55000, '', 250000),
('TPS005', 'MOTO', 'Honda Trx250x1', '2', 'DISPONIBLE', '19.0 km/l.', '2023-12-31', '2023-12-31', '2023-12-31', 28000, '', 170000),
('TPS006', 'MOTO', 'Polaris Sportman', '2', 'DISPONIBLE', '15 km/lt', '2023-12-31', '2023-12-31', '2023-12-31', 45000, '', 150000),
('TPS007', 'CARRO', 'CAN AM', '2', 'DISPONIBLE', '12 KML', '2023-12-31', '2023-12-31', '2023-12-31', 150000, '', 140000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitaciones`
--

CREATE TABLE `habitaciones` (
  `idhabitacion` int(14) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `capacidad` int(2) DEFAULT NULL,
  `precio` int(10) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `foto` varchar(30) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `habitaciones`
--

INSERT INTO `habitaciones` (`idhabitacion`, `tipo`, `descripcion`, `capacidad`, `precio`, `estado`, `foto`, `borrado`) VALUES
(101, 'ESTANDAR', 'BAÑO + WIFI', 2, 120000, 'DISPONIBLE', 'E20231206121445.png', 0),
(102, 'DE LUJO', 'BAÑO + WIFI', 4, 200000, 'DISPONIBLE', 'E20231206121519.png', 0),
(104, 'SUITE', 'BAÑO + WIFI', 4, 320000, 'DISPONIBLE', 'E20231206121601.png', 0),
(201, 'CABAÑA', 'BAÑO + WIFI + COCINA', 16, 550000, 'DISPONIBLE', 'E20231206121706.png', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login`
--

CREATE TABLE `login` (
  `usuario` varchar(20) NOT NULL,
  `password` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `login`
--

INSERT INTO `login` (`usuario`, `password`) VALUES
('usuario', '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idProd` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `cantidad` int(10) NOT NULL,
  `precio` int(10) NOT NULL,
  `iva` float NOT NULL,
  `estado` varchar(50) NOT NULL,
  `foto` varchar(50) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`idProd`, `nombre`, `descripcion`, `cantidad`, `precio`, `iva`, `estado`, `foto`, `borrado`) VALUES
(3, 'LIMPIEZA CUARTO', 'SERVICIO', 1, 50000, 0.19, 'DISPONIBLE', 'E20231206115858.png', 0),
(4, 'SPAY BELLEZA', 'SERVICIO', 1, 45000, 0.19, 'DISPONIBLE', 'E20231206115840.png', 0),
(6, 'CAFE MOLIDO', 'PRODUCTO', 1, 15000, 0.19, 'DISPONIBLE', 'E20231206120402.png', 0),
(7, 'PASEO ECOLOGICO', 'SERVICIO', 1, 35000, 0.19, 'DISPONIBLE', 'E20231206124147.png', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro`
--

CREATE TABLE `registro` (
  `idregistro` int(10) NOT NULL,
  `idhabitacion` int(14) NOT NULL,
  `idcliente` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  `precio` int(10) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro`
--

INSERT INTO `registro` (`idregistro`, `idhabitacion`, `idcliente`, `fecha_inicio`, `fecha_final`, `precio`, `borrado`) VALUES
(1, 38879331, '101', '2023-12-06', '2023-12-08', 120000, 0),
(2, 1115802400, '102', '2023-12-04', '2023-12-06', 250000, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `idreserva` int(10) NOT NULL,
  `idcliente` varchar(150) NOT NULL,
  `idhabitacion` int(14) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_final` date NOT NULL,
  `cant_personas` int(10) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `idServicio` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `duracion` varchar(50) NOT NULL,
  `precio` varchar(50) NOT NULL,
  `iva` float NOT NULL,
  `estado` varchar(50) NOT NULL,
  `foto` varchar(20) NOT NULL,
  `borrado` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`idServicio`, `nombre`, `descripcion`, `duracion`, `precio`, `iva`, `estado`, `foto`, `borrado`) VALUES
(1, 'LIMPIEZA', 'Servicio de limpieza a la habitación', '1', '15000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(2, 'PELUQUERIA', 'Servicio de peluqueria a nuestros clientes', '1', '15000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(3, 'SPA', 'Masaje corporal  y cuidado de la piel.', '1', '35000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(5, 'GUIA TURÍSTICO', 'Servicio de guia turistico ', '1', '15000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(6, 'PASEO ECOLÓGICO', 'Paseo alrededor del lago Calima.', '1', '45000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(7, 'MAQUILLAJE', 'Maquillaje con personal profesional.', '1', '28000', 0.19, 'DISPONIBLE', 'servicio.png', 0),
(8, 'SERVICIO AL CUARTO', 'Entrega de articulos de consumo.', '1', '25000', 0.19, 'DISPONIBLE', 'E20231130232335.png', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `idventa` int(10) NOT NULL,
  `idcomanda` int(10) NOT NULL,
  `idcodigo` varchar(20) NOT NULL,
  `descripItem` varchar(30) NOT NULL,
  `idregistro` varchar(20) NOT NULL,
  `idcliente` varchar(30) NOT NULL,
  `idhabitacion` varchar(10) NOT NULL,
  `fecha` date NOT NULL,
  `cantidad` int(10) NOT NULL,
  `valor` int(10) NOT NULL,
  `subtotal` int(10) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `borrado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idcliente`),
  ADD KEY `clixnac` (`nacionalidad`);

--
-- Indices de la tabla `comandas`
--
ALTER TABLE `comandas`
  ADD PRIMARY KEY (`idcomanda`),
  ADD KEY `idregistro` (`idregistro`),
  ADD KEY `idhabitacion` (`idhabitacion`),
  ADD KEY `descripItem` (`descripItem`);

--
-- Indices de la tabla `comunicaciones`
--
ALTER TABLE `comunicaciones`
  ADD PRIMARY KEY (`Idcomunicacion`),
  ADD KEY `idcliente` (`idcliente`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`idFactura`),
  ADD KEY `idRegistro` (`idRegistro`);

--
-- Indices de la tabla `gest_alqui`
--
ALTER TABLE `gest_alqui`
  ADD PRIMARY KEY (`id_alqui`),
  ADD KEY `placaxplaca` (`placa`);

--
-- Indices de la tabla `gest_vehic`
--
ALTER TABLE `gest_vehic`
  ADD PRIMARY KEY (`id_placa`);

--
-- Indices de la tabla `habitaciones`
--
ALTER TABLE `habitaciones`
  ADD PRIMARY KEY (`idhabitacion`);

--
-- Indices de la tabla `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`usuario`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idProd`);

--
-- Indices de la tabla `registro`
--
ALTER TABLE `registro`
  ADD PRIMARY KEY (`idregistro`),
  ADD KEY `idhabitacion` (`idhabitacion`,`idcliente`),
  ADD KEY `idcliente` (`idcliente`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`idreserva`),
  ADD KEY `idcliente` (`idcliente`,`idhabitacion`),
  ADD KEY `idhabitacion` (`idhabitacion`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`idServicio`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`idventa`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `gest_alqui`
--
ALTER TABLE `gest_alqui`
  MODIFY `id_alqui` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `idreserva` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `idventa` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
