package com.example.server;

import jakarta.jws.WebService;
import java.util.ArrayList;
import java.util.List;

@WebService
public class LibroService {
    private List<Libro> libros = new ArrayList<>();
    private int contador = 1;

    public String agregarLibro(String titulo, String autor, int anio, String editorial) {
        Libro libro = new Libro(contador++, titulo, autor, anio, editorial);
        libros.add(libro);
        return "Libro agregado: " + libro.getTitulo();
    }

    public List<Libro> listarLibros() {
        return libros;
    }

    public String actualizarLibro(int id, String titulo, String autor, int anio, String editorial) {
        for (Libro libro : libros) {
            if (libro.getId() == id) {
                libro.setTitulo(titulo);
                libro.setAutor(autor);
                libro.setAnio(anio);
                libro.setEditorial(editorial);
                return "Libro actualizado: " + libro.getTitulo();
            }
        }
        return "Libro no encontrado.";
    }

    public String eliminarLibro(int id) {
        libros.removeIf(libro -> libro.getId() == id);
        return "Libro eliminado.";
    }
}
