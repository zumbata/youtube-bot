@extends('layouts.default', ['title' => 'Log'])
@section('content')
    <div class="row justify-content-center text-center">
        <div class="col-6 card card-signin my-5">
            <h3 class="mt-2">Log</h3>
            <div class="row">
            <a href="/admin/log/clear" class="btn mb-3 btn-lg btn-primary btn-block text-uppercase w-50 mx-auto">Clear Log</a>
            @foreach ($lines as $line)
                <div class="col-12 mt-2">
                    {{ $line }}
                </div>
            @endforeach
            </div>
        </div>
    </div>
@stop