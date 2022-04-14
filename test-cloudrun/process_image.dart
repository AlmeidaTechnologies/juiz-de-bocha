import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<http.ByteStream> _processImageReturnImage(Uint8List bytes) async {
  http.Request request = http.Request(
    'POST',
    Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/image')
  );
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return response.stream;
}


Future<String> _processImageReturnURL(Uint8List bytes) async {
  http.Request request = http.Request(
    'POST',
    Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/url')
  );
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return await response.stream.bytesToString();
}



Future<String> processImageReturnURL(File img) async {
  return await processImage(await img.readAsBytes());
}

Future<File> processImageReturnImage(File foto, String pathResultado) async {
  File res = File(pathResultado);
  IOSink writeStream = res.openWrite();
  await writeStream.addStream(await _processImage(await foto.readAsBytes()));
  await writeStream.close();
  return res;
}
