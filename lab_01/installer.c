#include <stdio.h>
#include <stdlib.h>

#define CODESTART "\n\
#include <stdio.h>\n\
#include <stdlib.h>\n\
#include <string.h>\n\
#include <math.h>\n\
\n\
void getMachineId(char id[128]) {\n\
  system(\"ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\\\\\" \\'/IOPlatformUUID/{print tolower($(NF-1))}\' > id.txt\");\n\
\n\
  FILE *file = fopen(\"id.txt\", \"r\");\n\
\n\
  fscanf(file, \"%s\", id);\n\
\n\
  fclose(file);\n\
  system(\"rm id.txt\");\n\
}\n\
\n\
int main(void) {\n\
  char id[128];\n\
  getMachineId(id);\n\
\n\
  if (strcmp(id, \""

#define CODEEND "\") == 0) {\n\
    printf(\"--Access granted--\\n\\n\");\n\
  } else {\n\
    printf(\"--Access denied--\\n\\n\");\n\
    return 1;\n\
  }\n\
\n\
  float a, b, c, p, s;\n\
  printf(\"Calculate the area of a triangle\\n\");\n\
\n\
  printf(\"Input triangle sides: \");\n\
  scanf(\"%f %f %f\", &a, &b, &c);\n\
\n\
  if ((a + b <= c) || (a + c <= b) || (b + c <= a)) {\n\
    printf(\"Non-existent triangle\\n\");\n\
    return 1;\n\
  }\n\
\n\
  p = (a + b + c) / 2;\n\
  s = sqrt(p * (p - a) * (p - b) * (p - c));\n\
  printf(\"The area of the triangle is %0.2f\\n\", s);\n\
}\n"

void getMachineId(char id[128]) {
  system("ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" \'/IOPlatformUUID/{print tolower($(NF-1))}\' > id.txt");

  FILE *file = fopen("id.txt", "r");

  fscanf(file, "%s", id);

  fclose(file);
  system("rm id.txt");
}

int main(void) {
  FILE *program = fopen("main.c", "w");
  char id[128];
  getMachineId(id);

  fprintf(program, "%s", CODESTART);
  fprintf(program, "%s", id);
  fprintf(program, "%s", CODEEND);

  fclose(program);

  system("gcc main.c -o main");
  system("rm main.c");
}