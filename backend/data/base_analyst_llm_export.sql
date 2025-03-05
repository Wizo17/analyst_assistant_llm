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
    agency_id text,
    agency_name text,
    agency_url text,
    agency_timezone text,
    agency_lang double precision,
    agency_phone double precision,
    agency_email double precision,
    agency_fare_url text,
    ticketing_deep_link_id text
);


ALTER TABLE public.agency OWNER TO postgres;

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
    service_id text,
    monday bigint,
    tuesday bigint,
    wednesday bigint,
    thursday bigint,
    friday bigint,
    saturday bigint,
    sunday bigint,
    start_date bigint,
    end_date bigint
);


ALTER TABLE public.calendar OWNER TO postgres;

--
-- Name: calendar_dates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendar_dates (
    service_id text,
    date bigint,
    exception_type bigint
);


ALTER TABLE public.calendar_dates OWNER TO postgres;

--
-- Name: pathways; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pathways (
    pathway_id text,
    from_stop_id text,
    to_stop_id text,
    pathway_mode bigint,
    is_bidirectional bigint,
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
-- Name: routes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.routes (
    route_id text,
    agency_id text,
    route_short_name text,
    route_long_name text,
    route_desc double precision,
    route_type bigint,
    route_url double precision,
    route_color text,
    route_text_color text,
    route_sort_order double precision
);


ALTER TABLE public.routes OWNER TO postgres;

--
-- Name: stop_extensions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stop_extensions (
    object_id text,
    object_system text,
    object_code text
);


ALTER TABLE public.stop_extensions OWNER TO postgres;

--
-- Name: stop_times; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stop_times (
    trip_id text,
    arrival_time text,
    departure_time text,
    start_pickup_drop_off_window double precision,
    end_pickup_drop_off_window double precision,
    stop_id text,
    stop_sequence bigint,
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
-- Name: stops; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stops (
    stop_id text,
    stop_code double precision,
    stop_name text,
    stop_desc double precision,
    stop_lon double precision,
    stop_lat double precision,
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
    from_stop_id text,
    to_stop_id text,
    transfer_type bigint,
    min_transfer_time bigint
);


ALTER TABLE public.transfers OWNER TO postgres;

--
-- Name: trips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trips (
    route_id text,
    service_id text,
    trip_id text,
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
-- PostgreSQL database dump complete
--

