package school.sptech;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.DayOfWeek;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Maquina {
    private Integer idCaixaEletronico;
    private String dataHora;

    @JsonProperty("tempo_atividade")
    private Double tempoAtividade;

    @JsonProperty("porcCPU")
    private Double porcentagemCPU;

    @JsonProperty("freqCpu")
    private Double frequenciaCPU;

    @JsonProperty("usadaMem")
    private Double memoriaUsada;

    @JsonProperty("porcMem")
    private Double porcentagemMemoria;

    @JsonProperty("upload_kbps")
    private Double velocidadeUpload;

    @JsonProperty("download_kbps")
    private Double velocidadeDowload;

    public Integer getIdCaixaEletronico() {
        return idCaixaEletronico;
    }

    public void setIdCaixaEletronico(Integer idCaixaEletronico) {
        this.idCaixaEletronico = idCaixaEletronico;
    }

    public String getDataHora() {
        return dataHora;
    }

    public void setDataHora(String dataHora) {
        this.dataHora = dataHora;
    }

    public Double getTempoAtividade() {
        return tempoAtividade;
    }

    public void setTempoAtividade(Double tempoAtividade) {
        this.tempoAtividade = tempoAtividade;
    }

    public Double getPorcentagemCPU() {
        return porcentagemCPU;
    }

    public void setPorcentagemCPU(Double porcentagemCPU) {
        this.porcentagemCPU = porcentagemCPU;
    }

    public Double getFrequenciaCPU() {
        return frequenciaCPU;
    }

    public void setFrequenciaCPU(Double frequenciaCPU) {
        this.frequenciaCPU = frequenciaCPU;
    }

    public Double getMemoriaUsada() {
        return memoriaUsada;
    }

    public void setMemoriaUsada(Double memoriaUsada) {
        this.memoriaUsada = memoriaUsada;
    }

    public Double getPorcentagemMemoria() {
        return porcentagemMemoria;
    }

    public void setPorcentagemMemoria(Double porcentagemMemoria) {
        this.porcentagemMemoria = porcentagemMemoria;
    }

    public Double getVelocidadeUpload() {
        return velocidadeUpload;
    }

    public void setVelocidadeUpload(Double velocidadeUpload) {
        this.velocidadeUpload = velocidadeUpload;
    }

    public Double getVelocidadeDowload() {
        return velocidadeDowload;
    }

    public void setVelocidadeDowload(Double velocidadeDowload) {
        this.velocidadeDowload = velocidadeDowload;
    }

    public Maquina() {
    }

    public String getData() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        LocalDateTime dateTime = LocalDateTime.parse(this.dataHora, formatter);
        return dateTime.format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));
    }

    public String getHora() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        LocalDateTime dateTime = LocalDateTime.parse(dataHora, formatter);
        return dateTime.format(DateTimeFormatter.ofPattern("HH:mm:ss"));
    }

    public String getDiaDaSemana() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        LocalDateTime dateTime = LocalDateTime.parse(this.dataHora, formatter);
        DayOfWeek diaDaSemana = dateTime.getDayOfWeek();

        Locale locale = new Locale("pt", "BR");
        String diaDaSemanaTexto = diaDaSemana.getDisplayName(java.time.format.TextStyle.FULL, locale);
        diaDaSemanaTexto = diaDaSemanaTexto.substring(0, 1).toUpperCase().concat(diaDaSemanaTexto.substring(1));

        return diaDaSemanaTexto;
    }

    public Double getTempoEmMinutos() {
        return (double) Math.round(this.tempoAtividade / 60);
    }
}
