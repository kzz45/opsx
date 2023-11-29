<template>
    <el-form  label-width="100px" class="demo-dynamic">
    <el-form-item
        v-for="(label, index) in labels"
        label="标签"
        :key="index"
    >
        <el-input v-model="label.value" placeholder="键名=值"></el-input>
        <el-button @click="addLabel" type="primary"><i class="el-icon-plus"></i></el-button>
        <el-button @click.prevent="removeLabel(index)" type="danger"><i class="el-icon-minus"></i></el-button>
    </el-form-item>
    
    
    <!-- <el-form-item>
        <el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>
        <el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
    </el-form-item> -->
    </el-form>
</template>

<script>
  export default {
    name: 'ResourceLabel',
    props: {
      labels: { required: true, type: Array },
    },
    data() {
      return {
      };
    },
    methods: {
    //  submitForm(formName) {
    //     this.$refs[formName].validate((valid) => {
    //       if (valid) {
    //         alert('submit!');
    //       } else {
    //         console.log('error submit!!');
    //         return false;
    //       }
    //     });
    //   },
    //   resetForm(formName) {
    //     this.$refs[formName].resetFields();
    //   },
      removeLabel(index) {
          this.labels.splice(index, 1)
      },
      addLabel() {
        this.labels.push({
          value: '',
        });
        this.$emit('change', this.labels)
      }
    }
  }
</script>

<style scoped>
.el-input {
  width: 300px;
  margin-right: 5px;
}
</style>