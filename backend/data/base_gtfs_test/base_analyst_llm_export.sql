--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agency; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agency (
    agency_id text NOT NULL,
    agency_name text NOT NULL,
    agency_url text NOT NULL,
    agency_timezone text NOT NULL,
    agency_lang double precision,
    agency_phone double precision,
    agency_email double precision,
    agency_fare_url text,
    ticketing_deep_link_id text
);


ALTER TABLE public.agency OWNER TO postgres;

--
-- Name: TABLE agency; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.agency IS 'Réseau commercial';


--
-- Name: COLUMN agency.agency_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_id IS 'Identifiant du réseau
Exemple de valeur : IDFM:XXX';


--
-- Name: COLUMN agency.agency_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_name IS 'Nom commercial du réseau
La liste des réseaux commerciaux inclus les noms commerciaux des réseaux de transport de bus et les groupes de lignes par mode METRO, TRAMWAY, RER, TER, TRAIN, Navette (cdgval, Funiculaire, Orlyval)';


--
-- Name: COLUMN agency.agency_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_url IS 'URL de l''agence de transports en commun';


--
-- Name: COLUMN agency.agency_timezone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_timezone IS 'Fuseau horaire de la zone où se trouve l’agence
Exemple : Europe/Paris';


--
-- Name: COLUMN agency.agency_lang; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_lang IS 'Langue parlée de l’agence';


--
-- Name: COLUMN agency.agency_phone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_phone IS 'Numéro de téléphone de l’agence';


--
-- Name: COLUMN agency.agency_email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_email IS 'Adresse email consultée par le service client de
l’agence';


--
-- Name: COLUMN agency.agency_fare_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.agency.agency_fare_url IS 'URL qui redirige sur la rubrique "titre et tarifs dusite web Ile-de-France Mobilités';


--
-- Name: booking_rules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booking_rules (
    id text,
    booking_type bigint,
    message text,
    phone_number text,
    info_url text,
    booking_url text
);


ALTER TABLE public.booking_rules OWNER TO postgres;

--
-- Name: calendar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendar (
    service_id text NOT NULL,
    monday bigint NOT NULL,
    tuesday bigint NOT NULL,
    wednesday bigint NOT NULL,
    thursday bigint NOT NULL,
    friday bigint NOT NULL,
    saturday bigint NOT NULL,
    sunday bigint NOT NULL,
    start_date bigint NOT NULL,
    end_date bigint NOT NULL
);


ALTER TABLE public.calendar OWNER TO postgres;

--
-- Name: COLUMN calendar.service_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.service_id IS 'Identifiant du calendrier de circulation';


--
-- Name: COLUMN calendar.monday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.monday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.tuesday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.tuesday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.wednesday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.wednesday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.thursday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.thursday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.friday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.friday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.saturday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.saturday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.sunday; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.sunday IS 'Jours de fonctionnement de la course sur la période
1 circule
0 ne circule pas';


--
-- Name: COLUMN calendar.start_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.start_date IS 'Début de la période (AAAAMMJJ)';


--
-- Name: COLUMN calendar.end_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar.end_date IS 'Fin de la période (AAAAMMJJ)';


--
-- Name: calendar_dates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendar_dates (
    service_id text NOT NULL,
    date bigint NOT NULL,
    exception_type bigint NOT NULL
);


ALTER TABLE public.calendar_dates OWNER TO postgres;

--
-- Name: COLUMN calendar_dates.service_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar_dates.service_id IS 'Identifiant du calendrier de circulation
Exemple : IDFM:XXX ou IDFM:TN:XXX pour les objets SNCF';


--
-- Name: COLUMN calendar_dates.date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar_dates.date IS 'Jours en exception (AAAAMMJJ)';


--
-- Name: COLUMN calendar_dates.exception_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.calendar_dates.exception_type IS 'Type d’exception
1 = circule aussi à cette date
2 = ne circule pas à cette date';


--
-- Name: pathways; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pathways (
    pathway_id text NOT NULL,
    from_stop_id text NOT NULL,
    to_stop_id text NOT NULL,
    pathway_mode bigint NOT NULL,
    is_bidirectional bigint NOT NULL,
    length double precision,
    traversal_time bigint,
    stair_count double precision,
    max_slope double precision,
    min_width double precision,
    signposted_as double precision,
    reversed_signposted_as double precision
);


ALTER TABLE public.pathways OWNER TO postgres;

--
-- Name: COLUMN pathways.pathway_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.pathway_id IS 'Identifiant du chemin';


--
-- Name: COLUMN pathways.from_stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.from_stop_id IS 'Emplacement du départ du chemin';


--
-- Name: COLUMN pathways.to_stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.to_stop_id IS 'Emplacement d’arrivée du chemin';


--
-- Name: COLUMN pathways.pathway_mode; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.pathway_mode IS 'Type de chemin pour la paire spécifiée (from_stop_id, to_stop_id)
1 : voie piétonne,
 2 : escalier, 
3 : tapis roulant, 
4 : escalier mécanique, 
5 : ascenseur, 
6 : porte de validation du titre de transport';


--
-- Name: COLUMN pathways.is_bidirectional; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.is_bidirectional IS 'Indique dans quel sens les usagers peuvent emprunter le chemin
0: chemin unidirectionnel de from_stop_id à to_stop_id
1 : chemin bidirectionnel';


--
-- Name: COLUMN pathways.length; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.length IS 'Longueur du chemin en mètre (sens horizontal)';


--
-- Name: COLUMN pathways.traversal_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.traversal_time IS 'Durée moyenne pour parcourir le chemin de from_stop_id à to_stop_id';


--
-- Name: COLUMN pathways.stair_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.stair_count IS 'Nombre de marche d’escalier à gravir sur le chemin';


--
-- Name: COLUMN pathways.max_slope; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.max_slope IS '• 0 ou vide : pas de pente
• Nombre à virgule flottante : pourcentage de pente du chemin, positif pour une montée et négatif pour une descente';


--
-- Name: COLUMN pathways.min_width; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.min_width IS 'Largeur minimal du chemin en mètre';


--
-- Name: COLUMN pathways.signposted_as; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.signposted_as IS 'Chaîne de texte correspondant exactement aux panneaux affichés auprès des usagers du service de transports en commun';


--
-- Name: COLUMN pathways.reversed_signposted_as; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.pathways.reversed_signposted_as IS 'Identique à signposted_as, mais il est utilisé lorsque le chemin est parcouru en sens inverse';


--
-- Name: routes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.routes (
    route_id text NOT NULL,
    agency_id text NOT NULL,
    route_short_name text NOT NULL,
    route_long_name text NOT NULL,
    route_desc double precision,
    route_type bigint NOT NULL,
    route_url double precision,
    route_color text,
    route_text_color text,
    route_sort_order double precision
);


ALTER TABLE public.routes OWNER TO postgres;

--
-- Name: TABLE routes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.routes IS 'Lignes de transport';


--
-- Name: COLUMN routes.route_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_id IS 'Identifiant de la ligne
Exemple : IDFM:CXXXXX';


--
-- Name: COLUMN routes.agency_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.agency_id IS 'Identifiant du réseau
Exemple : IDFM:XXX';


--
-- Name: COLUMN routes.route_short_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_short_name IS 'Nom court de la ligne';


--
-- Name: COLUMN routes.route_long_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_long_name IS 'Nom long de la ligne';


--
-- Name: COLUMN routes.route_desc; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_desc IS 'Description d’un itinéraire';


--
-- Name: COLUMN routes.route_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_type IS 'Mode de la ligne
0 –Tramway | 1 – Métro | 2 – Train | 3 – Bus | 7 - Funiculaire';


--
-- Name: COLUMN routes.route_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_url IS 'URL d’une page web pour un itinéraire';


--
-- Name: COLUMN routes.route_color; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_color IS 'Code couleur de la ligne
000000(noir) si couleur non connue';


--
-- Name: COLUMN routes.route_text_color; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_text_color IS 'Code couleur du texte de la ligne
FFFFFF (blanc) si couleur non connue';


--
-- Name: COLUMN routes.route_sort_order; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.routes.route_sort_order IS 'Ordre de présentation des itinéraires(plus petit en premier)';


--
-- Name: stop_extensions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stop_extensions (
    object_id text NOT NULL,
    object_system text,
    object_code text
);


ALTER TABLE public.stop_extensions OWNER TO postgres;

--
-- Name: COLUMN stop_extensions.object_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_extensions.object_id IS 'Identifiant du StopPoint';


--
-- Name: COLUMN stop_extensions.object_system; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_extensions.object_system IS 'Type du StopPoint';


--
-- Name: COLUMN stop_extensions.object_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_extensions.object_code IS 'Identifiant type';


--
-- Name: stop_times; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stop_times (
    trip_id text NOT NULL,
    arrival_time text NOT NULL,
    departure_time text NOT NULL,
    start_pickup_drop_off_window double precision,
    end_pickup_drop_off_window double precision,
    stop_id text NOT NULL,
    stop_sequence bigint NOT NULL,
    pickup_type bigint,
    drop_off_type bigint,
    local_zone_id double precision,
    stop_headsign double precision,
    timepoint bigint,
    pickup_booking_rule_id text,
    drop_off_booking_rule_id text
);


ALTER TABLE public.stop_times OWNER TO postgres;

--
-- Name: COLUMN stop_times.trip_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.trip_id IS 'Identifiant de la course';


--
-- Name: COLUMN stop_times.arrival_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.arrival_time IS 'Heure d’arrivée à l’arrêt (HH:MM:SS)';


--
-- Name: COLUMN stop_times.departure_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.departure_time IS 'Heure de départ à l’arrêt (HH:MM:SS)';


--
-- Name: COLUMN stop_times.stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.stop_id IS 'Identifiant de l’arrêt';


--
-- Name: COLUMN stop_times.stop_sequence; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.stop_sequence IS 'Numéro d’ordre de l’arrêt dans la course
avec 0 = 1 er arrêt de la course';


--
-- Name: COLUMN stop_times.pickup_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.pickup_type IS 'Indique les possibilités de montée à bord
0 ou vide = montée autorisée
1 = montée interdite';


--
-- Name: COLUMN stop_times.drop_off_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.drop_off_type IS 'Indique les possibilités de descente du véhicule
0 ou vide = descente autorisée
1 = descente interdit';


--
-- Name: COLUMN stop_times.stop_headsign; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.stop_headsign IS 'Texte qui apparaît sur la signalétique indiquant aux usagers la destination du trajet';


--
-- Name: COLUMN stop_times.timepoint; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stop_times.timepoint IS 'Indique si les heures spécifiées pour un arrêt sont strictement respectées
0 = horaires approximatifs
1 ou vide = horaires exacts';


--
-- Name: stops; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stops (
    stop_id text NOT NULL,
    stop_code double precision,
    stop_name text NOT NULL,
    stop_desc double precision,
    stop_lon double precision NOT NULL,
    stop_lat double precision NOT NULL,
    zone_id double precision,
    stop_url double precision,
    location_type bigint,
    parent_station text,
    stop_timezone text,
    level_id double precision,
    wheelchair_boarding bigint,
    platform_code double precision
);


ALTER TABLE public.stops OWNER TO postgres;

--
-- Name: COLUMN stops.stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_id IS 'Identifiant de l’arrêt physique';


--
-- Name: COLUMN stops.stop_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_code IS 'Texte court ou numéro identifiant l''emplacement pour les usagers';


--
-- Name: COLUMN stops.stop_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_name IS 'Nom de l’arrêt ou de l’accès';


--
-- Name: COLUMN stops.stop_desc; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_desc IS 'Description de l’emplacement';


--
-- Name: COLUMN stops.stop_lon; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_lon IS 'Longitude de l’arrêt ou de l’accès';


--
-- Name: COLUMN stops.stop_lat; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_lat IS 'Latitude de l’arrêt ou de l’accès';


--
-- Name: COLUMN stops.zone_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.zone_id IS 'Zone tarifaire (uniquement pour les objets StopPoint)
1, 2, 3, 4, 5,
100 = non renseigné,
101 = Hors Zone Ile-de-France';


--
-- Name: COLUMN stops.stop_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_url IS 'URL d''une page Web qui décrit l''emplacement';


--
-- Name: COLUMN stops.location_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.location_type IS 'Type d’emplacement
Arrêt physique (StopPoint) = 0
Arrêt commercial (StopArea) = 1
Accès station (Station Entrance) = 2';


--
-- Name: COLUMN stops.parent_station; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.parent_station IS 'Arrêt « parent » (identifiant de l’arrêt commercial auquel est rattaché l’arrêt physique ou l’accès)';


--
-- Name: COLUMN stops.stop_timezone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.stop_timezone IS 'Fuseau horaire de l’emplacement';


--
-- Name: COLUMN stops.level_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.level_id IS 'Etage où se trouve l’emplacement';


--
-- Name: COLUMN stops.wheelchair_boarding; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.wheelchair_boarding IS 'Accessibilité UFR (uniquement pour les objets StopPoint)
0 = Non renseigné
1 = Accessible UFR*
2 = Non accessible UFR';


--
-- Name: COLUMN stops.platform_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.stops.platform_code IS 'Identifiant du quai pour un arrêt qui se situe dans une station';


--
-- Name: ticketing_deep_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ticketing_deep_links (
    ticketing_deep_link_id text,
    web_url text,
    android_intent_uri text,
    ios_universal_link_url text
);


ALTER TABLE public.ticketing_deep_links OWNER TO postgres;

--
-- Name: transfers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transfers (
    from_stop_id text NOT NULL,
    to_stop_id text NOT NULL,
    transfer_type bigint NOT NULL,
    min_transfer_time bigint
);


ALTER TABLE public.transfers OWNER TO postgres;

--
-- Name: COLUMN transfers.from_stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.transfers.from_stop_id IS 'Premier arrêt physique en correspondance';


--
-- Name: COLUMN transfers.to_stop_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.transfers.to_stop_id IS 'Second arrêt physique en correspondance';


--
-- Name: COLUMN transfers.transfer_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.transfers.transfer_type IS 'Indique le type de correspondance pour la paire (from_stop_id, to_stop_id) spécifiée';


--
-- Name: COLUMN transfers.min_transfer_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.transfers.min_transfer_time IS 'Durée de correspondance à pieds (en secondes)';


--
-- Name: trips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trips (
    route_id text NOT NULL,
    service_id text NOT NULL,
    trip_id text NOT NULL,
    trip_headsign text,
    trip_short_name text,
    direction_id bigint,
    block_id double precision,
    shape_id double precision,
    wheelchair_accessible bigint,
    bikes_allowed bigint
);


ALTER TABLE public.trips OWNER TO postgres;

--
-- Name: COLUMN trips.route_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.route_id IS 'Identifiant de la ligne';


--
-- Name: COLUMN trips.service_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.service_id IS 'Identifiant du calendrier de circulation';


--
-- Name: COLUMN trips.trip_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.trip_id IS 'Identifiant de la course';


--
-- Name: COLUMN trips.trip_headsign; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.trip_headsign IS 'Libellé du dernier arrêt de la course pour tous les modes de transport';


--
-- Name: COLUMN trips.trip_short_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.trip_short_name IS 'Train/RER : code mission
Métro/Bus/tram : non renseigné';


--
-- Name: COLUMN trips.direction_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.direction_id IS 'Direction du trajet
1 = Aller
0 = Retour';


--
-- Name: COLUMN trips.block_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.block_id IS 'Identifie le block auquel appartient le trajet';


--
-- Name: COLUMN trips.shape_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.shape_id IS 'Définit une forme géospatiale décrivant le parcours du véhicule lors d''un trajet';


--
-- Name: COLUMN trips.wheelchair_accessible; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.wheelchair_accessible IS 'Accessibilité UFR (uniquement pour les objets StopPoint)
0 = Non renseigné
1 = Accessible UFR*
2 = Non accessible UFR';


--
-- Name: COLUMN trips.bikes_allowed; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.trips.bikes_allowed IS 'Indique si les vélos sont autorisés pour le trajet spécifié
0 = Aucune information
1 = Au moins un vélo
2 = Aucun vélo';


--
-- PostgreSQL database dump complete
--

