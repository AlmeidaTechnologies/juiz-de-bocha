import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;


/// ResultURLs: classe para resultado em URLs do processamento do algoritmo
/// Como usar:
///
///   Converter uma string em json para o resultado:
///     ResultURLs resultado = ResultURLs.fromJsonString(stringEmJson);
///
///   Converter Map para o resultado:
///     ResultURLs resultado = ResultURLs.fromJson(dadosEmMap);
///
///   Converter o resultado para o formato json - Map:
///     Map<String, dynamic> resultadoEmJson = resultado.toJson();
///
///   Converter o resultado para string json:
///     String resultadoEmStringJson = resultado.toJsonString();
///
class ResultURLs {
  /// resultado em gif
  final String animated;
  /// resultado em tamanho reduzido para mostrar em lista
  final String thumbnail;

  const ResultURLs(this.animated, this.thumbnail);

  /// cria o resultado a partir de string json
  factory ResultURLs.fromJsonString(String json) => ResultURLs.fromJson(jsonDecode(json));

  /// cria o resultado a partir de json em Map
  ResultURLs.fromJson(Map<String, dynamic> json)
      : animated = json['gif'] ?? json['animated'],
        thumbnail = json['thumbnail'];

  /// cria um json em Map do resultado atual
  Map<String, dynamic> toJson() => {
    'animated': animated,
    'thumbnail': thumbnail,
  };

  /// cria um json em String do resultado atual
  String toJsonString() => jsonEncode(toJson());

  /// no print, mostra os dados da classe
  String toString() => "Classe ResultsURLs:\n\t{"
    "\n\t\tanimated: \"$animated,\""
    "\n\t\tthumbnail: \"$thumbnail\""
  "\n\t}";

}


/// Funcao interna ///
Future<String> __makeRequest(
    String endpoint,
    Map<String, dynamic> queryParameters,
    Uint8List bytes
) async {
  // setup uri //
  final Uri uri = Uri
      .parse('https://recognizer-usnztkx52q-rj.a.run.app$endpoint')
      .replace(queryParameters: queryParameters);
  // uri = uri.replace();
  // setup request //
  http.Request request = http.Request('POST', uri);
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  // send data //
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  // process and return response //
  return response.stream.bytesToString();
}


/// Funcao pra ser utilizada ///
Future<ResultURLs> processarImagem(
    File img,
    {
      String? userID,
      double? accelerometer,
      double? gyroscope,
      double? lensAperture,
      double? sensorSensitivity,
      int? sensorExposureTime,
    }
) async {
  String response = await __makeRequest(
    '/url',
    {
      'userID': userID,
      'accelerometer': accelerometer.toString(),
      'gyroscope': gyroscope.toString(),
      'lensAperture': lensAperture.toString(),
      'sensorSensitivity': sensorSensitivity.toString(),
      'sensorExposureTime': sensorExposureTime.toString(),
      'with-thumbnail': 'true',
    },
    await img.readAsBytes(),
  );
  return ResultURLs.fromJsonString(response);
}


/// Exemplo de uso ///
void main(){
  File img = File('test.jpg');
  processarImagem(
    img,
    userID: "1",
    accelerometer: 2.9,
  ).then((ResultURLs resultado){
    print("resultado: $resultado");
  });
}
