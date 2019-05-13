/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author rhaps
 */
@WebServlet(urlPatterns = {"/ServletExample"})
public class ServletExample extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
            /* TODO output your page here. You may use following sample code. */
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet ServletExample</title>");            
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet ServletExample at " + request.getContextPath() + "</h1>");
            out.println("</body>");
            out.println("</html>");
        }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        //processRequest(request, response);
        PrintWriter out = response.getWriter();
        String title ="Pagina de saludo";        
        // selecciona el contenido de la respuesta
        response.setContentType("text/html");
        // escribimos el contenido de la respuesta
        out.println("<HTML>"
                + "<HEAD> <TITLE> ");
        out.println(title);
        out.println("</TITLE> </HEAD><BODY>");
        out.println("<H1>"+title+"</H1>");
        out.println("<BR>");
        out.println("<form method='POST'>");
        out.println("<center> What do you want for vacations?");
        out.println("<BR>");
        out.println("<input type='text' name='gift'>");
        out.println("<input type='submit' value='submit'>");
        out.println("<BR>");
        out.println("</center>");
        out.println("</form>");
        
		
	
        // obtiene el nombre del cliente de la solicitud
        String nombreUsuario = request.getParameter("nombre");
        if(nombreUsuario != null)
        {
            out.println("<P>Hola GET: "+nombreUsuario+"</P>");
            
        }
        out.println("</BODY></HTML>");
        out.close();
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        //processRequest(request, response);
        String gift = request.getParameter("gift");
        PrintWriter out = response.getWriter();
        response.setContentType("text/html");
        out.println("<HTML><HEAD><TITLE> RESPUESTA POST </TITLE></HEAD>");
        out.println("<BODY>");
        out.println("<H1>Respuesta: " +gift+"</H1>");
        out.println("</BODY>");
        out.println("</HTML>");
        out.close();
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
