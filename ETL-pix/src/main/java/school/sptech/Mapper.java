package school.sptech;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public abstract class Mapper {
    abstract List<Pix> map(InputStream inputStream) throws IOException;
}
