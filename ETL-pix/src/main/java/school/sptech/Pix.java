package school.sptech;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.util.Date;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Pix {

    @JsonProperty("AnoMes")
    private String data;


    @JsonProperty("PAG_REGIAO")
    private String regiaoPagamento;

    @JsonProperty("REC_REGIAO")
    private String regiaoRecebimento;

    @JsonProperty("PAG_IDADE")
    private String idadePagamento;

    @JsonProperty("REC_IDADE")
    private String idadeRecebimento;

    @JsonProperty("VALOR")
    private Double valor;

    @JsonProperty("QUANTIDADE")
    private Integer quantidade;

    public String getData() {
        String data = this.data;
        YearMonth mesAno = YearMonth.parse(data, DateTimeFormatter.ofPattern("yyyyMM"));
        String dataFormatada = mesAno.format(DateTimeFormatter.ofPattern("MM-yyyy"));

        return dataFormatada;
    }
    public void setData(String data) {
        this.data = data;
    }

    public String getRegiaoPagamento() {
        return regiaoPagamento;
    }
    public void setRegiaoPagamento(String regiaoPagamento) {
        this.regiaoPagamento = regiaoPagamento;
    }

    public String getRegiaoRecebimento() {
        return regiaoRecebimento;
    }
    public void setRegiaoRecebimento(String regiaoRecebimento) {
        this.regiaoRecebimento = regiaoRecebimento;
    }

    public String getIdadePagamento() {
        return idadePagamento;
    }
    public void setIdadePagamento(String idadePagamento) {
        this.idadePagamento = idadePagamento;
    }

    public String getIdadeRecebimento() {
        return idadeRecebimento;
    }
    public void setIdadeRecebimento(String idadeRecebimento) {
        this.idadeRecebimento = idadeRecebimento;
    }

    public Double getValor() {
        return valor;
    }
    public void setValor(Double valor) {
        this.valor = valor;
    }

    public Integer getQuantidade() {
        return quantidade;
    }
    public void setQuantidade(Integer quantidade) {
        this.quantidade = quantidade;
    }

    public Double getPrecoTransacao() {
        Double precoTransacional = valor / quantidade;
        Double precoFormatado = Double.parseDouble("%.2f".formatted(precoTransacional).replace(',','.'));

        return precoFormatado;
    }

    @Override
    public String toString() {
        return "Pix{" +
                "data='" + data + '\'' +
                ", regiaoPagamento='" + regiaoPagamento + '\'' +
                ", regiaoRecebimento='" + regiaoRecebimento + '\'' +
                ", idadePagamento=" + idadePagamento +
                ", idadeRecebimento=" + idadeRecebimento +
                ", valor=" + valor +
                ", quantidade=" + quantidade +
                '}';
    }
}
