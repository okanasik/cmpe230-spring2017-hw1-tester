#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main(int argc, char** argv) {
	if (argc == 1) {
		cerr << "you should provide statement file " << endl;
	} else if (argc == 2) {
		string input_file_name = argv[1];
		string output_file_name = input_file_name.substr(0,input_file_name.find("."));
		output_file_name.append(".ll");
		ofstream output_file(output_file_name.c_str());
		if (output_file.is_open()) {
			output_file << "; ModuleID = 'stm2ir'"<< endl;
			output_file << "declare i32 @printf(i8*, ...)"<< endl;
			output_file << "@print.str = constant [4 x i8] c\"%d\\0A\\00\""<< endl;
			output_file << "define i32 @main() {"<< endl;
			output_file << "%k = alloca i32"<< endl;
			output_file << "%x1 = alloca i32"<< endl;
			output_file << "%y = alloca i32"<< endl;
			output_file << "%zvalue = alloca i32"<< endl;
			output_file << "store i32 3, i32* %x1"<< endl;
			output_file << "%1 = udiv i32 11,2"<< endl;
			output_file << "store i32 %1, i32* %y"<< endl;
			output_file << "%2 = load i32* %x1"<< endl;
			output_file << "%3 = load i32* %y"<< endl;
			output_file << "%4 = add i32 1,%3"<< endl;
			output_file << "%5 = mul i32 %2,%4"<< endl;
			output_file << "%6 = add i32 23,%5"<< endl;
			output_file << "store i32 %6, i32* %zvalue"<< endl;
			output_file << "%7 = load i32* %zvalue"<< endl;
			output_file << "call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0), i32 %7 )"<< endl;
			output_file << "%9 = load i32* %x1"<< endl;
			output_file << "%10 = load i32* %y"<< endl;
			output_file << "%11 = sub i32 %9,%10"<< endl;
			output_file << "%12 = load i32* %zvalue"<< endl;
			output_file << "%13 = sub i32 %11,%12"<< endl;
			output_file << "store i32 %13, i32* %k"<< endl;
			output_file << "%14 = load i32* %x1"<< endl;
			output_file << "%15 = load i32* %y"<< endl;
			output_file << "%16 = mul i32 3,%15"<< endl;
			output_file << "%17 = add i32 2,5"<< endl;
			output_file << "%18 = mul i32 1,%17"<< endl;
			output_file << "%19 = mul i32 %16,%18"<< endl;
			output_file << "%20 = add i32 %14,%19"<< endl;
			output_file << "store i32 %20, i32* %k"<< endl;
			output_file << "%21 = load i32* %k"<< endl;
			output_file << "%22 = add i32 %21,1"<< endl;
			output_file << "call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0), i32 %22 )" << endl;
			output_file << "ret i32 0"<<endl;
			output_file << "}"<< endl;
			output_file.close();
		}
	}
	return 0;
}
