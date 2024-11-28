package school.sptech;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.List;

public class Main implements RequestHandler<S3Event, String> {

    // Criação do cliente S3 para acessar os buckets
    private final AmazonS3 s3Client = AmazonS3ClientBuilder.defaultClient();

    // Bucket de destino para o CSV gerado
    private static final String DESTINATION_BUCKET = "bucket-trusted-passini";

    @Override
    public String handleRequest(S3Event s3Event, Context context) {

        // Extraímos o nome do bucket de origem e a chave do arquivo JSON
        String sourceBucket = s3Event.getRecords().get(0).getS3().getBucket().getName();
        String sourceKey = s3Event.getRecords().get(0).getS3().getObject().getKey();

        try {
            InputStream s3InputStream = s3Client.getObject(sourceBucket, sourceKey).getObjectContent();

            List<Pix> pixs;

            if (sourceKey.endsWith(".csv")){
                System.out.println("Mapper CSV acionado");
                MapperCSV mapper = new MapperCSV();
                pixs = mapper.map(s3InputStream);
            } else{
                System.out.println("Mapper JSON acionado");
                MapperJson mapper = new MapperJson();
                pixs = mapper.map(s3InputStream);
            }

            CsvWriter csvWriter = new CsvWriter();
            ByteArrayOutputStream csvOutputStream = csvWriter.writeCsv(pixs);

            InputStream csvInputStream = new ByteArrayInputStream(csvOutputStream.toByteArray());

            s3Client.putObject(DESTINATION_BUCKET, sourceKey.replace(".json", ".csv"), csvInputStream, null);

            return "Sucesso no processamento";
        } catch (Exception e) {
            context.getLogger().log("Erro: " + e.getMessage());
            return "Erro no processamento";
        }
    }
}