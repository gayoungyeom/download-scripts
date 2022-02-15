from flask import Flask, render_template, request, flash, send_file
import download
import zipfile, os

# Flak 앱 서버 인스턴스
app = Flask(__name__)
app.secret_key = "abcde"

# url 패턴 - 라우팅 - 데코레이터
@app.route('/')
def index():
    #get을 통해 전달받은 데이터 확인
    title = request.args.get('title')
    format = request.args.get('format') or "docx"

    if title:
        res = download.get_episodes(title)
        status = res.get('status')
        episodes = res.get('episodes')

        if status == 404:
            flash("해당 대본이 존재하지 않거나, 제목이 올바르지 않습니다.")
        else:    
            download.get_scripts(title, episodes, format)
            # 압축하기
            # path = f'static/scripts/{title}'
            with zipfile.ZipFile(f'static/scripts/{title}/{title}.zip', 'w') as script_zip:
                for (path, dir, files) in os.walk(f'static/scripts/{title}'):
                    for file in files:
                        if file.endswith(f'.{format}'):
                            script_zip.write(f'{path}/{file}', os.path.relpath(f'{path}/{file}', f'static/scripts/{title}'), compress_type = zipfile.ZIP_DEFLATED) 
            return send_file(f'static/scripts/{title}/{title}.zip', mimetype='zip', attachment_filename=f'static/scripts/{title}/{title}.zip', as_attachment=True)  
    return render_template('index.html')

# 메인 테스트
if __name__ == '__main__':
    app.run(debug=True)
    