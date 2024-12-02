package school.sptech;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;

public interface EscritorArquivo {
    ByteArrayOutputStream escreverArquivo(List<Maquina> maquinas) throws IOException;
}