package com.example.server;

import jakarta.xml.ws.Endpoint;

public class Main {
    public static void main(String[] args) {
        String url = "http://localhost:8080/LibrosService";
        Endpoint.publish(url, new LibroService());
        System.out.println("Servidor SOAP corriendo en " + url + "?wsdl");
    }
}
