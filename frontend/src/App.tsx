import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";
import { ReactNode } from "react";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";

interface Args {
  schema: Record<string, any>;
  uiSchema: Record<string, any>;
  userData: Record<string, any> | null;
}
class JsonformComponent extends StreamlitComponentBase {
  public state = { formData: null as Record<string, any> | null };
  public render = (): ReactNode => {
    const { schema, uiSchema, userData }: Args = this.props.args;

    if (userData) this.state.formData = userData;
    return (
      <Form
        schema={schema}
        validator={validator}
        uiSchema={uiSchema}
        onSubmit={this._submitFormData}
        onChange={(e) => {
          this.state.formData = e.formData;
        }}
        formData={this.state.formData}
      />
    );
  };
  private _submitFormData = (formData: any): void => {
    Streamlit.setComponentValue({
      errors: formData.errors,
      formData: formData.formData,
      schemaValidationErrors: formData.schemaValidationErrors,
    });
  };
}

export default withStreamlitConnection(JsonformComponent);
