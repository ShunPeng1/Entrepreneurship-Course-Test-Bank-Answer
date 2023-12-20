from PyPDF2 import PdfReader
import re

def extract_questions(pdf_file : PdfReader):
    questions = []
    for page_num in range(len(pdf_file.pages)):
        page_text = pdf_file.pages[page_num].extract_text()
        page_text_decoded = page_text.encode('latin-1', 'replace').decode('utf-8', 'replace')
        
        matches = re.findall(r"(\d+\))(.+?)(Answer: (.{2,100}))", page_text, re.DOTALL)
        for match in matches:
            question_number, question_content, answer_block, answer = match
            
            try:
                if any("A" in answer[i] for i in range(1, 5)):
                    answer = question_content.split("A)")[1]
                if any("B" in answer[i] for i in range(1, 5)):
                    answer = question_content.split("B)")[1]
                if any("C" in answer[i] for i in range(1, 5)):
                    answer = question_content.split("C)")[1]
                if any("D" in answer[i] for i in range(1, 5)):
                    answer = question_content.split("D)")[1]
                if any("E" in answer[i] for i in range(1, 5)):
                    answer = question_content.split("E)")[1]
                elif "TRUE" in answer:
                    answer = "TRUE"
                elif "FALSE" in answer:
                    answer = "FALSE"
                else:
                    raise Exception("Invalid answer: {}".format(answer))
            
            except Exception as e:
                answer = answer


            if page_num == 45:
                print(question_number)
                print(question_content)
                print(answer_block)
                print(answer)
                
                
            question_content = question_content.split("\n")[0]
            answer = answer.split("\n")[0]

            

            questions.append({
                "page": page_num + 1,
                "question_number": question_number.strip(),
                "question_content": question_content.strip(),
                "answer": answer.strip()
            })


    return questions

def generate_index(questions, index_filename):
    questions.sort(key=lambda x: x["question_content"])
    with open(index_filename, 'w') as index_file:
        for pair in questions:
            index_file.write("[{}] {} {}\n".format(pair["page"], " " * (3 - len(str(pair["page"]))), pair["question_content"]))
            index_file.write("Answer: {}\n".format(pair["answer"]))
            


def main():
    try:
        pdf_reader = PdfReader("test-bank_pagenumber.pdf")
    except FileNotFoundError:
        print("Error: PDF file not found.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    questions_list = extract_questions(pdf_reader)
    generate_index(questions_list, 'index.txt')

    print("Done!")

if __name__ == "__main__":
    main()
