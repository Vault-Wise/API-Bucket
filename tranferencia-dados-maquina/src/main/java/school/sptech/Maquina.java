package school.sptech;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

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

    @JsonProperty("totalMem")
    private Double totalMemoria;

    @JsonProperty("usadaMem")
    private Double memoriaUsada;

    @JsonProperty("porcMem")
    private Double porcentagemMemoria;

    @JsonProperty("totalDisc")
    private Double totalDisco;

    @JsonProperty("usadoDisc")
    private Double discoUsado;

    @JsonProperty("porcDisc")
    private Double porcentagemDisco;

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

    public Double getTotalMemoria() {
        return totalMemoria;
    }

    public void setTotalMemoria(Double totalMemoria) {
        this.totalMemoria = totalMemoria;
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

    public Double getTotalDisco() {
        return totalDisco;
    }

    public void setTotalDisco(Double totalDisco) {
        this.totalDisco = totalDisco;
    }

    public Double getDiscoUsado() {
        return discoUsado;
    }

    public void setDiscoUsado(Double discoUsado) {
        this.discoUsado = discoUsado;
    }

    public Double getPorcentagemDisco() {
        return porcentagemDisco;
    }

    public void setPorcentagemDisco(Double porcentagemDisco) {
        this.porcentagemDisco = porcentagemDisco;
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
}
