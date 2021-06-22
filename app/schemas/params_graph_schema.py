from marshmallow import Schema, fields, pre_load, pre_dump
import json
class ParamsGraphScham(Schema):
    dataInicial = fields.Date(required=True)
    dataFinal = fields.Date(required=True)
    rankingClientesPor = fields.Int(required=True)
    tiposServicosPor = fields.Int(required=True)

class ChartVendas(Schema):
    data = fields.String(required=True)
    valor = fields.Float(required=True)
    @pre_dump
    def validate(self, data, **kwargs):

        return {
            'data': data[0],
            'valor': data[1]
        }

class ChartCancelados(Schema):
    data = fields.String(required=True)
    quantidade = fields.Int(required=True)

class ChartRankingClientes(Schema):
    id = fields.Int(required=True)
    nome = fields.String(required=True)
    valor = fields.Float(required=True)
    quantidade = fields.Int(required=True)


class ChartTiposServicos(Schema):
    id = fields.Int(required=True)
    descricao = fields.String(required=True)
    valor = fields.Float(required=True)
    quantidade = fields.Int(required=True)

