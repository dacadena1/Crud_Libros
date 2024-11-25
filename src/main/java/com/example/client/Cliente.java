package com.example.client;

import com.example.server.LibroService;
import com.example.server.Libro;

public class Cliente {
    public static void main(String[] args) {
        LibroService service = new LibroService();
        LibroService port = service.getLibroServicePort();

        // Agregar libros
        System.out.println(port.agregarLibro("Libro 1", "Autor 1", 2023, "Editorial X"));

        // Listar libros
        System.out.println(port.listarLibros());

        // Actualizar libro
        System.out.println(port.actualizarLibro(1, "Libro 1 Actualizado", "Autor 1", 2023, "Editorial Y"));

        // Eliminar libro
        System.out.println(port.eliminarLibro(1));
    }
}
